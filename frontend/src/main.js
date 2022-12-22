import Vue from 'vue'
import App from './App.vue'
import './index.css'
import 'roboto-fontface/css/roboto/roboto-fontface.css'
import '@mdi/font/css/materialdesignicons.css'
import '@/plugins/index'

Vue.config.productionTip = false

new Vue({
  render: h => h(App)
}).$mount('#app')
