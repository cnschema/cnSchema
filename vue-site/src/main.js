// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import { Pagination,Menu,MenuItem,Input,Table,TableColumn,Tabs,TabPane,Icon,Autocomplete,Tree,Row,Col } from 'element-ui'
import 'element-ui/lib/theme-default/index.css'
import util from './assets/util'
import VueResource from 'vue-resource';
import selfCompenent from './assets/components/'

Vue.config.productionTip = false
Vue.use(util)
Vue.use(VueResource)
Vue.use(selfCompenent)

/*element ui*/

Vue.use(Pagination)
Vue.use(Menu)
Vue.use(Input)
Vue.use(Table)
Vue.use(Tabs)
Vue.use(TabPane)
Vue.use(Icon)
Vue.use(Autocomplete)
Vue.use(Tree)
Vue.use(Row)
Vue.use(Col)
Vue.use(MenuItem)
Vue.use(TableColumn)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})
