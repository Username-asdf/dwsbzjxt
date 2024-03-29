import Vue from 'vue'
import Router from 'vue-router'
import animal from "./components/animal";
import rules from "./components/animal/rules";
// 导入公共样式表
import '../src/assets/resert.css'

Vue.use(Router)

export default new Router({
  routes: [
    // {
    //   path: '/',
    //   name: 'bestLocation',
    //   component: bestLocation
    // },
    {
      path: '/',
      name: 'animal',
      component: animal
    },
    {
      path: '/rules',
      name: 'rules',
      component: rules
    },
  ]
})
