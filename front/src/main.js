import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import './assets/landingpagemain.css';

const app = createApp(App);
app.use(router);
app.mount('#app');

import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

// اضيفي هنا الأيقونة لي تحتاجيها
import { faDribbble } from '@fortawesome/free-brands-svg-icons'
import { faChartLine } from '@fortawesome/free-solid-svg-icons'

// نضيفو الأيقونات لمكتبتي
library.add(faDribbble)
library.add(faChartLine)

// const app = createApp(App)

app.component('FontAwesomeIcon', FontAwesomeIcon)

// app.mount('#app')