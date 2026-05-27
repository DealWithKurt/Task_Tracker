import { createRouter, createWebHashHistory } from 'vue-router';
import TaskList from '../pages/TaskList.vue';
import TaskDetail from '../pages/TaskDetail.vue';
import Login from '../pages/Login.vue';
import Register from '../pages/Register.vue';
import { useAuthStore } from '../stores/auth';

const routes = [
    { path: '/', component: TaskList, meta: { requiresAuth: true } },
    { path: '/tasks/:id', component: TaskDetail, meta: { requiresAuth: true } },
    { path: '/login', component: Login },
    { path: '/register', component: Register },
];

const router = createRouter({
    history: createWebHashHistory(),
    routes,
});

router.beforeEach((to, from) => {
    const authStore = useAuthStore();
    if (to.meta.requiresAuth && !authStore.token) {
        return '/login';
    }
    return true;
});

export default router;