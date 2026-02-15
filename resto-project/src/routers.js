import Vue from 'vue';
import Home from './components/Home.vue';
import SignUp from './components/SignUp.vue';
import VueRouter from 'vue-router';

Vue.use(VueRouter);
const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/signup',
        name: 'SignUp',
        component: SignUp
    }
];

const router = new VueRouter({
    mode: 'history',
    routes
});

export default router;
