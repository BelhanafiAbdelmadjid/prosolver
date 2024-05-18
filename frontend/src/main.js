import { createApp } from 'vue'
import App from './App.vue'
import routes from './route'
import { createRouter,createWebHistory  } from 'vue-router'
import { createPinia } from 'pinia'

import mitt from 'mitt'
const emitter = mitt();

const router = new createRouter({
    mode : "hash",
    history: createWebHistory(),
    routes, // short for `routes: routes`
})

const pinia = createPinia()
const app = createApp(App)

app.config.globalProperties.emitter = emitter;
app.use(pinia);
app.use(router);
app.mount('#app');

export default {router , emitter}
