import Vue from 'vue';
import Home from './components/Home.vue';
import SignUp from './components/SignUp.vue';
import Login from './components/Login.vue';
import MenuManagement from './components/MenuManagement.vue';
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
    },
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
    {
        path: '/menu-management',
        name: 'MenuManagement',
        component: MenuManagement
    }
];

const router = new VueRouter({
    mode: 'history',
    routes
});

export default router;
