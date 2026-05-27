import { defineStore } from 'pinia';
import { login, fetchMe, register } from '../api/auth';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        token: localStorage.getItem('token') || null,
        user: null,
    }),
    actions: {
        async login(credentials) {
            const res = await login(credentials);
            this.token = res.data.access_token;
            localStorage.setItem('token', this.token);
            await this.fetchUser();
        },
        async register(data) {
            await register(data);
            await this.login({ email: data.email, password: data.password });
        },
        async fetchUser() {
            if (!this.token) return;
            try {
                const res = await fetchMe();
                this.user = res.data;
            } catch (e) {
                this.logout();
            }
        },
        logout() {
            this.token = null;
            this.user = null;
            localStorage.removeItem('token');
        }
    }
});
