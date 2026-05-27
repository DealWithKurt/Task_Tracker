<template>
  <div>
    <nav v-if="authStore.token" class="navbar">
      <router-link to="/" class="navbar-brand">
        <span class="logo-icon">✓</span>
        Task Tracker
      </router-link>
      <div class="navbar-right">
        <span class="navbar-user" v-if="authStore.user">
          <strong>{{ authStore.user.name }}</strong>
          <span style="margin-left: 0.25rem; opacity: 0.7">({{ roleName(authStore.user.role) }})</span>
        </span>
        <button class="btn btn-ghost btn-sm" @click="logout">Выйти</button>
      </div>
    </nav>
    <router-view></router-view>
  </div>
</template>

<script setup>
import { useAuthStore } from './stores/auth';
import { useRouter } from 'vue-router';
import { onMounted } from 'vue';

const authStore = useAuthStore();
const router = useRouter();

const roleName = (role) => {
  const names = { admin: 'Админ', user: 'Пользователь', guest: 'Гость' };
  return names[role] || role;
};

onMounted(async () => {
  if (authStore.token) {
    try {
      await authStore.fetchUser();
    } catch (e) {
      authStore.logout();
      router.push('/login');
    }
  }
});

const logout = () => {
  authStore.logout();
  router.push('/login');
};
</script>