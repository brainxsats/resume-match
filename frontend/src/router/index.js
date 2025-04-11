import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Report from '../views/Report.vue'
import Summary from '../views/Summary.vue'

Vue.use(VueRouter)

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/report',
      name: 'report',
      component: Report
    },
    {
      path: '/summary',
      name: 'summary',
      component: Summary
    }
  ]
})

export default router 