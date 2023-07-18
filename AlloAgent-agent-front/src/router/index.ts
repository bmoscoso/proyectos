import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import MainBase from '../views/MainBase.vue'
import MainInicio from '../views/Inicio/MainInicio.vue'
import CrudAgents from '../views/CrudAgents.vue'
import Dashboard from '../views/Dashboard.vue'

Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
  {
    path: '/',
    name: 'home',
    component: MainBase,
    children: [
      {
        path: '/home/inicio',
        name: 'MainInicio',
        component: MainInicio
      },
      { /* Nosotros */
        path: '/home/inicio/agents',
        name: 'CrudAgents',
        component: CrudAgents
      },
      { /* Nosotros */
        path: '/home/inicio/dashboard',
        name: 'Dashboard',
        component: Dashboard
      },
    ] 
  }
]

const router = new VueRouter({
  routes
})

export default router
