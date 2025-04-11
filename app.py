from fastapi import FastAPI, Request, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
import json
from typing import Dict
import httpx
import asyncio
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import io

# 加载配置文件
load_dotenv('config.env')

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 设置OpenAI API密钥
openai.api_key = os.getenv("OPENAI_API_KEY")

# Dify API配置
DIFY_API_URL = "http://chat.bitboy.cc/v1/chat-messages"
DIFY_API_KEY = os.getenv("DIFY_API_KEY")
DIFY_REPORT_API_KEY = os.getenv("DIFY_REPORT_API_KEY")

@app.post("/api/analyze")
async def analyze_resume(request: Request):
    try:
        data = await request.json()
        resume = data.get("resume", "")
        job = data.get("job", "")

        # 构建提示词
        prompt = f"""请分析以下简历与职位描述的匹配度，并给出详细的分析报告。

职位描述：
{job}

简历内容：
{resume}
根据以上信息，进行深入的分析直接输出报告不要对话
"""

        async def generate_response():
            try:
                response = await openai.ChatCompletion.acreate(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "你是一个专业的简历分析专家，请对简历和职位进行匹配分析，并使用Markdown格式输出结果。"},
                        {"role": "user", "content": prompt}
                    ],
                    stream=True
                )

                async for chunk in response:
                    if chunk and chunk.choices and chunk.choices[0].delta.get("content"):
                        content = chunk.choices[0].delta["content"]
                        yield f"data: {json.dumps({'content': content})}\n\n"

            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"

        return StreamingResponse(
            generate_response(),
            media_type="text/event-stream"
        )

    except Exception as e:
        return {"error": str(e)}

@app.post("/api/analyze-dify-summary")
async def analyze_resume_dify(request: Request):
    try:
        data = await request.json()
        resume = data.get("resume", "")
        job = data.get("job", "")
        report = data.get("report", "")

        # 构建提示词
        prompt = f"""请分析以下简历,职位以及报告，并给出详细的总结报告。

职位描述：
{job}

简历内容：
{resume}

简历匹配报告
{report}

根据以上信息，进行深入的分析直接输出报告不要对话
"""

        async def generate_response():
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        DIFY_API_URL,
                        headers={
                            "Authorization": f"Bearer {DIFY_REPORT_API_KEY}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "inputs": {},
                            "query": prompt,
                            "response_mode": "streaming",
                            "conversation_id": "",
                            "user": "resume-analyzer"
                        },
                        timeout=60.0
                    )
                    
                    if response.status_code != 200:
                        yield f"data: {json.dumps({'error': f'API请求失败: {response.status_code}'})}\n\n"
                        return
                    
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            try:
                                data = json.loads(line[6:])
                                if "answer" in data:
                                    yield f"data: {json.dumps({'content': data['answer']})}\n\n"
                            except json.JSONDecodeError:
                                continue

            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"

        return StreamingResponse(
            generate_response(),
            media_type="text/event-stream"
        )

    except Exception as e:
        return {"error": str(e)}


@app.post("/api/analyze-dify")
async def analyze_resume_dify(request: Request):
    try:
        data = await request.json()
        resume = data.get("resume", "")
        job = data.get("job", "")

        # 构建提示词
        prompt = f"""请分析以下简历与职位，并给出详细的匹配度分析报告。

职位描述：
{job}

简历内容：
{resume}

根据以上信息，进行深入的分析直接输出报告不要对话
"""

        async def generate_response():
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        DIFY_API_URL,
                        headers={
                            "Authorization": f"Bearer {DIFY_API_KEY}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "inputs": {},
                            "query": prompt,
                            "response_mode": "streaming",
                            "conversation_id": "",
                            "user": "resume-analyzer"
                        },
                        timeout=60.0
                    )
                    
                    if response.status_code != 200:
                        yield f"data: {json.dumps({'error': f'API请求失败: {response.status_code}'})}\n\n"
                        return
                    
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            try:
                                data = json.loads(line[6:])
                                if "answer" in data:
                                    yield f"data: {json.dumps({'content': data['answer']})}\n\n"
                            except json.JSONDecodeError:
                                continue

            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"

        return StreamingResponse(
            generate_response(),
            media_type="text/event-stream"
        )

    except Exception as e:
        return {"error": str(e)}

@app.post("/api/extract-pdf")
async def extract_pdf(file: UploadFile = File(...)):
    try:
        # 读取上传的PDF文件
        contents = await file.read()
        pdf_file = io.BytesIO(contents)
        
        # 使用PyPDF2读取PDF内容
        pdf_reader = PdfReader(pdf_file)
        text_content = ""
        
        # 提取所有页面的文本
        for page in pdf_reader.pages:
            text_content += page.extract_text() + "\n"
        
        # 清理文本内容
        text_content = text_content.strip()
        
        if not text_content:
            raise HTTPException(status_code=400, detail="无法从PDF文件中提取文本内容")
        
        return {"content": text_content}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理PDF文件时出错: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 