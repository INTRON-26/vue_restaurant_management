import Vue from 'vue';
import Home from './components/Home.vue';
import SignUp from './components/SignUp.vue';
import Login from './components/Login.vue';
import MenuManagement from './components/MenuManagement.vue';
import MenuList from './components/MenuList.vue';
import ReservationForm from './components/ReservationForm.vue';
import MyReservations from './components/MyReservations.vue';
import ReservationDashboard from './components/ReservationDashboard.vue';
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
    },
    {
        path: '/menu',
        name: 'MenuList',
        component: MenuList
    },
    {
        path: '/reservations',
        name: 'Reservations',
        component: ReservationForm
    },
    {
        path: '/my-reservations',
        name: 'MyReservations',
        component: MyReservations,
        meta: { requiresRole: ['customer'] }
    },
    {
        path: '/reservation-dashboard',
        name: 'ReservationDashboard',
        component: ReservationDashboard,
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
