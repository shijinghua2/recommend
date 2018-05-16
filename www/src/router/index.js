import Vue from 'vue'
import Router from 'vue-router'

import PagesView from '../views/PagesView'
import BookView from '../views/BookView'
import SubjectView from '../views/SubjectView'
import LoginView from '../views/LoginView'
import RegisterView from '../views/RegisterView'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HomeView',
      redirect: '/pages/book'
    },
    {
      path: '/pages',
      component: PagesView,
      children: [
        {
          path: '',
          redirect: '/pages/book'
        },
        {
          path: 'book',
          name: 'BookView',
          component: BookView
        }
      ]
    },
    {
      path: '/pages/:classify/subject/:id',
      name: 'SubjectView',
      components: {
        default: PagesView,
        subject: SubjectView
      }
    },
    {
      path: '/login',
      name: 'LoginView',
      component: LoginView
    },
    {
      path: '/register',
      name: 'RegisterView',
      component: RegisterView
    },
    {
      path: '*',
      redirect: '/pages/'
    }
  ]
})
