<template>
  <div class="container">
    <div class="task-detail" v-if="task">
      <router-link to="/" class="btn btn-ghost btn-sm" style="margin-bottom: 1rem;">← Назад к задачам</router-link>
      
      <div class="detail-card">
        <div class="detail-header">
          <h1>{{ task.title }}</h1>
          <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
            <span :class="['badge', `badge-${task.status}`]">{{ statusName(task.status) }}</span>
            <span :class="['badge', `badge-${task.priority}`]">{{ priorityName(task.priority) }}</span>
          </div>
        </div>

        <div v-if="task.description" class="detail-field">
          <label>Описание</label>
          <div class="value">{{ task.description }}</div>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem;">
          <div class="detail-field">
            <label>Срок</label>
            <div class="value">{{ formatDate(task.deadline) }}</div>
          </div>
          <div class="detail-field">
            <label>Исполнитель</label>
            <div class="value">{{ task.assignee?.name || 'Не назначен' }}</div>
          </div>
          <div class="detail-field">
            <label>Создана</label>
            <div class="value">{{ formatDateTime(task.created_at) }}</div>
          </div>
          <div class="detail-field">
            <label>Обновлена</label>
            <div class="value">{{ formatDateTime(task.updated_at) }}</div>
          </div>
        </div>

        <div v-if="canEdit" class="detail-actions">
          <button class="btn btn-primary btn-sm" style="width: auto;" @click="showEdit = true">Редактировать</button>
          <button v-if="canDelete" class="btn btn-danger btn-sm" @click="delTask">Удалить</button>
        </div>
      </div>

      <!-- Модальное окно редактирования -->
      <div v-if="showEdit" class="modal-overlay" @click.self="showEdit = false">
        <div class="modal-content">
          <h2>Редактировать задачу</h2>
          <form @submit.prevent="saveEdit">
            <div class="form-group">
              <label>Название</label>
              <input v-model="editData.title" required minlength="3" />
            </div>
            <div class="form-group">
              <label>Описание</label>
              <textarea v-model="editData.description" rows="3" style="width: 100%; padding: 0.75rem 1rem; border: 2px solid #e5e7eb; border-radius: 12px; font-size: 0.95rem; font-family: inherit; resize: vertical;"></textarea>
            </div>
            <div class="form-group">
              <label>Статус</label>
              <select v-model="editData.status">
                <option value="new">Новая</option>
                <option value="in_progress">В работе</option>
                <option value="done">Готово</option>
                <option value="cancelled">Отменена</option>
              </select>
            </div>
            <div class="form-group">
              <label>Приоритет</label>
              <select v-model="editData.priority">
                <option value="low">Низкий</option>
                <option value="medium">Средний</option>
                <option value="high">Высокий</option>
              </select>
            </div>
            <div class="form-group">
              <label>Срок</label>
              <input v-model="editData.deadline" type="date" required />
            </div>
            <div class="modal-actions">
              <button type="button" class="btn btn-ghost" @click="showEdit = false">Отмена</button>
              <button type="submit" class="btn btn-primary" style="flex: 1;">Сохранить</button>
            </div>
          </form>
        </div>
      </div>

      <!-- Комментарии -->
      <div class="comments-section">
        <h3>Комментарии ({{ comments.length }})</h3>
        
        <div v-if="comments.length === 0" style="text-align: center; padding: 2rem; color: #9ca3af;">
          <p>Комментариев пока нет. Будьте первым!</p>
        </div>

        <div v-for="c in comments" :key="c.id" class="comment-item">
          <div class="comment-header">
            <span class="comment-author">{{ c.user?.name || 'Аноним' }}</span>
            <div style="display: flex; align-items: center; gap: 0.75rem;">
              <span class="comment-date">{{ formatDateTime(c.created_at) }}</span>
              <button v-if="canDeleteComment(c)" class="btn btn-ghost btn-sm" style="color: #ef4444; padding: 0.2rem 0.5rem;" @click="delComment(c.id)">✕</button>
            </div>
          </div>
          <div class="comment-text">{{ c.text }}</div>
        </div>

        <form v-if="canEdit" class="comment-form" @submit.prevent="addComment">
          <input v-model="newComment" placeholder="Написать комментарий..." required />
          <button type="submit" class="btn btn-primary btn-sm" style="width: auto; white-space: nowrap;" :disabled="!newComment.trim()">Отправить</button>
        </form>
      </div>
    </div>

    <div v-else style="text-align: center; padding: 3rem;">
      <div class="spinner" style="width: 40px; height: 40px; margin: 0 auto;"></div>
      <p style="margin-top: 1rem; color: #6b7280;">Загрузка задачи...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { getTask, updateTask, deleteTask, getComments, createComment, deleteComment } from '../api/tasks';
import { useAuthStore } from '../stores/auth';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const task = ref(null);
const comments = ref([]);
const showEdit = ref(false);
const editData = ref({ title: '', description: '', status: 'new', priority: 'medium', deadline: '' });
const newComment = ref('');

const canEdit = computed(() => authStore.user?.role !== 'guest');
const canDelete = computed(() => authStore.user?.role === 'admin');

const statusName = (s) => ({ new: 'Новая', in_progress: 'В работе', done: 'Готово', cancelled: 'Отменена' }[s] || s);
const priorityName = (p) => ({ low: 'Низкий', medium: 'Средний', high: 'Высокий' }[p] || p);

const loadData = async () => {
  try {
    const [t, c] = await Promise.all([
      getTask(route.params.id),
      getComments(route.params.id)
    ]);
    task.value = t.data;
    comments.value = c.data;
    editData.value = {
      title: t.data.title,
      description: t.data.description || '',
      status: t.data.status,
      priority: t.data.priority,
      deadline: t.data.deadline,
    };
  } catch (e) {
    alert('Ошибка загрузки задачи');
  }
};

onMounted(loadData);

const saveEdit = async () => {
  try {
    await updateTask(task.value.id, editData.value);
    showEdit.value = false;
    loadData();
  } catch (e) {
    alert('Не удалось обновить задачу');
  }
};

const delTask = async () => {
  if (confirm('Вы уверены, что хотите удалить эту задачу?')) {
    try {
      await deleteTask(task.value.id);
      router.push('/');
    } catch (e) {
      alert('Не удалось удалить задачу');
    }
  }
};

const addComment = async () => {
  if (!newComment.value.trim()) return;
  try {
    await createComment(task.value.id, { text: newComment.value });
    newComment.value = '';
    loadData();
  } catch (e) {
    alert('Не удалось добавить комментарий');
  }
};

const canDeleteComment = (c) => {
  if (authStore.user?.role === 'admin') return true;
  return authStore.user?.role === 'user' && c.user_id === authStore.user?.id;
};

const delComment = async (id) => {
  if (confirm('Удалить комментарий?')) {
    try {
      await deleteComment(id);
      loadData();
    } catch (e) {
      alert('Не удалось удалить комментарий');
    }
  }
};

const formatDate = (dateStr) => {
  const d = new Date(dateStr);
  return d.toLocaleDateString('ru-RU', { month: 'short', day: 'numeric', year: 'numeric' });
};

const formatDateTime = (dateStr) => {
  const d = new Date(dateStr);
  return d.toLocaleDateString('ru-RU', { month: 'short', day: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit' });
};
</script>