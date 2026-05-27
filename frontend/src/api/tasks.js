import api from './index';

export const getTasks = (params) => api.get('/tasks', { params });
export const getTask = (id) => api.get(`/tasks/${id}`);
export const createTask = (data) => api.post('/tasks', data);
export const updateTask = (id, data) => api.put(`/tasks/${id}`, data);
export const deleteTask = (id) => api.delete(`/tasks/${id}`);

export const getComments = (taskId) => api.get(`/tasks/${taskId}/comments`);
export const createComment = (taskId, data) => api.post(`/tasks/${taskId}/comments`, data);
export const deleteComment = (id) => api.delete(`/comments/${id}`);
