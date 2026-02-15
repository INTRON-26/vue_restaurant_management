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
        component: MenuManagement,
        meta: { requiresRole: ['admin', 'staff'] }
    }
];

const router = new VueRouter({
    mode: 'history',
    routes
});

router.beforeEach((to, from, next) => {
    const requiredRoles = to.meta?.requiresRole;
    if (!requiredRoles) {
        return next();
    }

    const token = localStorage.getItem('accessToken');
    const role = localStorage.getItem('userRole');
    if (!token) {
        return next('/login');
    }

    if (!requiredRoles.includes(role)) {
        return next('/');
    }

    return next();
});

export default router;
