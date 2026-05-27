<template>
  <div class="auth-page">
    <div class="auth-card">
      <div style="text-align: center; margin-bottom: 0.5rem;">
        <div class="navbar-brand" style="justify-content: center; font-size: 1.5rem; margin-bottom: 0.5rem;">
          <span class="logo-icon">✓</span>
          Task Tracker
        </div>
      </div>
      <h2>Создать аккаунт</h2>
      <p class="subtitle">Присоединяйтесь к управлению задачами</p>
      
      <div v-if="error" class="alert alert-error">{{ error }}</div>
      
      <form @submit.prevent="submit">
        <div class="form-group">
          <label>Имя</label>
          <input v-model="name" placeholder="Ваше полное имя" required />
        </div>
        <div class="form-group">
          <label>Эл. почта</label>
          <input v-model="email" type="email" placeholder="your@email.com" required />
        </div>
        <div class="form-group">
          <label>Пароль</label>
          <input v-model="password" type="password" placeholder="Минимум 4 символа" required minlength="4" />
        </div>
        <button type="submit" class="btn btn-primary" :disabled="loading">
          <span v-if="loading" class="spinner"></span>
          <span v-else>Создать аккаунт</span>
        </button>
      </form>
      <p class="auth-link">
        Уже есть аккаунт? <router-link to="/login">Войти</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';

const name = ref('');
const email = ref('');
const password = ref('');
const error = ref('');
const loading = ref(false);
const authStore = useAuthStore();
const router = useRouter();

const submit = async () => {
  error.value = '';
  loading.value = true;
  try {
    await authStore.register({ name: name.value, email: email.value, password: password.value });
    router.push('/');
  } catch (e) {
    error.value = 'Ошибка регистрации. Возможно, email уже используется.';
  } finally {
    loading.value = false;
  }
};
</script>