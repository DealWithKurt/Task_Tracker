<template>
  <div class="container">
    <div class="page-header">
      <h1>Задачи</h1>
      <button v-if="canCreate" class="btn btn-primary" style="width: auto; padding: 0.6rem 1.25rem;" @click="showCreateModal = true">
        + Новая задача
      </button>
    </div>

    <div class="filters-bar">
      <input v-model="filters.search" placeholder="Поиск задач..." @input="debouncedSearch" />
      <select v-model="filters.status" @change="loadTasks">
        <option value="">Все статусы</option>
        <option value="new">Новая</option>
        <option value="in_progress">В работе</option>
        <option value="done">Готово</option>
        <option value="cancelled">Отменена</option>
      </select>
      <select v-model="filters.priority" @change="loadTasks">
        <option value="">Все приоритеты</option>
        <option value="low">Низкий</option>
        <option value="medium">Средний</option>
        <option value="high">Высокий</option>
      </select>
    </div>

    <div v-if="loading" style="text-align: center; padding: 3rem;">
      <div class="spinner" style="width: 40px; height: 40px;"></div>
      <p style="margin-top: 1rem; color: #6b7280;">Загрузка задач...</p>
    </div>

    <div v-else-if="tasks.length === 0" class="empty-state">
      <div class="empty-icon"></div>
      <h3>Задачи не найдены</h3>
      <p>Создайте первую задачу, чтобы начать</p>
    </div>

    <div v-else class="task-grid">
      <div v-for="task in tasks" :key="task.id" class="task-card" @click="router.push(`/tasks/${task.id}`)">
        <h3>{{ task.title }}</h3>
        <p v-if="task.description">{{ task.description }}</p>
        <div class="task-meta">
          <span :class="['badge', `badge-${task.status}`]">{{ statusName(task.status) }}</span>
          <span :class="['badge', `badge-${task.priority}`]">{{ priorityName(task.priority) }}</span>
          <span v-if="task.deadline" class="task-date">{{ formatDate(task.deadline) }}</span>
        </div>
      </div>
    </div>

    <div v-if="totalPages > 1" class="pagination">
      <button class="btn btn-ghost btn-sm" :disabled="page <= 1" @click="changePage(page - 1)">← Назад</button>
      <span>Стр. {{ page }} из {{ totalPages }}</span>
      <button class="btn btn-ghost btn-sm" :disabled="page >= totalPages" @click="changePage(page + 1)">Вперёд →</button>
    </div>

    <!-- Модальное окно создания задачи -->
    <div v-if="showCreateModal" class="modal-overlay" @click.self="showCreateModal = false">
      <div class="modal-content">
        <h2>Создать задачу</h2>
        <form @submit.prevent="createTask">
          <div class="form-group">
            <label>Название *</label>
            <input v-model="newTask.title" placeholder="Название (мин. 3 символа)" required minlength="3" />
          </div>
          <div class="form-group">
            <label>Описание</label>
            <textarea v-model="newTask.description" placeholder="Описание (необязательно)" rows="3" style="width: 100%; padding: 0.75rem 1rem; border: 2px solid #e5e7eb; border-radius: 12px; font-size: 0.95rem; font-family: inherit; resize: vertical;"></textarea>
          </div>
          <div class="form-group">
            <label>Статус</label>
            <select v-model="newTask.status">
              <option value="new">Новая</option>
              <option value="in_progress">В работе</option>
              <option value="done">Готово</option>
              <option value="cancelled">Отменена</option>
            </select>
          </div>
          <div class="form-group">
            <label>Приоритет</label>
            <select v-model="newTask.priority">
              <option value="low">Низкий</option>
              <option value="medium">Средний</option>
              <option value="high">Высокий</option>
            </select>
          </div>
          <div class="form-group">
            <label>Срок *</label>
            <input v-model="newTask.deadline" type="date" required />
          </div>
          <div class="modal-actions">
            <button type="button" class="btn btn-ghost" @click="showCreateModal = false">Отмена</button>
            <button type="submit" class="btn btn-primary" style="flex: 1;">Создать</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useTaskStore } from '../stores/tasks';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const tasksStore = useTaskStore();
const authStore = useAuthStore();

const tasks = computed(() => tasksStore.tasks);
const loading = ref(false);
const page = ref(1);
const limit = 12;
const totalPages = ref(1);
const showCreateModal = ref(false);
const canCreate = computed(() => ['admin', 'user'].includes(authStore.user?.role));

const filters = reactive({
  search: '',
  status: '',
  priority: '',
});

const newTask = reactive({
  title: '',
  description: '',
  status: 'new',
  priority: 'medium',
  deadline: '',
});

const statusName = (s) => ({ new: 'Новая', in_progress: 'В работе', done: 'Готово', cancelled: 'Отменена' }[s] || s);
const priorityName = (p) => ({ low: 'Низкий', medium: 'Средний', high: 'Высокий' }[p] || p);

let searchTimeout = null;
const debouncedSearch = () => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    page.value = 1;
    loadTasks();
  }, 300);
};

const loadTasks = async () => {
  loading.value = true;
  try {
    const result = await tasksStore.fetchTasks({
      ...filters,
      page: page.value,
      limit,
    });
    totalPages.value = result.pages || 1;
  } catch (e) {
    console.error('Ошибка загрузки задач:', e);
  } finally {
    loading.value = false;
  }
};

const changePage = (newPage) => {
  page.value = newPage;
  loadTasks();
};

const createTask = async () => {
  try {
    await tasksStore.createTask({ ...newTask });
    showCreateModal.value = false;
    newTask.title = '';
    newTask.description = '';
    newTask.status = 'new';
    newTask.priority = 'medium';
    newTask.deadline = '';
    page.value = 1;
    await loadTasks();
  } catch (e) {
    alert('Не удалось создать задачу');
  }
};

const formatDate = (dateStr) => {
  const d = new Date(dateStr);
  return d.toLocaleDateString('ru-RU', { month: 'short', day: 'numeric', year: 'numeric' });
};

onMounted(loadTasks);
</script>