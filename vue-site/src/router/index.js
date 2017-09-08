import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  mode: 'history',
  scrollBehavior (to, from, savedPosition) {
    return { x: 0, y: 0 }
  },
  routes: [
    {
        path: '*',
        redirect: {name: '404'}
    },
    {
        path: '/404',
        name: '404',
        components: {
            main: resolve => {
                require(['@/components/notFound'],resolve)
            },
        }
    },
    {
        path: '/index',
        redirect: {name: 'desk'}
    },
    {
        path: '/',
        name: 'desk',
        components: {
            header: resolve => {
                require(['@/components/header'],resolve)
            },
            main: resolve => {
                require(['@/components/desk'],resolve)
            },
            footer: resolve => {
                require(['@/components/footer'],resolve)
            }
        }
    },
    {
        path: '/_cns_about',
        name: 'about',
        components: {
            header: resolve => {
                require(['@/components/header'],resolve)
            },
            main: resolve => {
                require(['@/components/about'],resolve)
            },
            footer: resolve => {
                require(['@/components/footer'],resolve)
            }
        },
        children: [{
            path: 'aboutus',
            name: 'aboutus',
            component: resolve => {
                require(['@/components/aboutus'],resolve)
            }
        },{
            path: 'people',
            name: 'people',
            component: resolve => {
                require(['@/components/people'],resolve)
            }
        },{
            path: 'contacts',
            name: 'contacts',
            component: resolve => {
                require(['@/components/contacts'],resolve)
            }
        }]
    },
    {
        path: '/_cns_vocab',
        name: 'dictionary',
        components: {
            header: resolve => {
                require(['@/components/header'],resolve)
            },
            main: resolve => {
                require(['@/components/dictionary'],resolve)
            }
        }
    },
    {
        path: '/:query',
        name: 'detail',
        components: {
            header: resolve => {
                require(['@/components/header'],resolve)
            },
            main: resolve => {
                require(['@/components/detail'],resolve)
            },
            footer: resolve => {
                require(['@/components/footer'],resolve)
            }
        }
    }
  ]
})


