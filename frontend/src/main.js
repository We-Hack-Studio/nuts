import '@babel/polyfill'
import 'mutationobserver-shim'
import './plugins/bootstrap-vue'
import './assets/base.scss';

import App from './App.vue'
import JsonEditor from 'vue-json-edit'
import ToggleButton from 'vue-js-toggle-button'
import Vue from 'vue'
import router from "./router";
import store from "./store";

Vue.use(ToggleButton)
Vue.use(JsonEditor)
Vue.config.productionTip = false

new Vue({
    render: h => h(App),
    router,
    store,
}).$mount('#app')
