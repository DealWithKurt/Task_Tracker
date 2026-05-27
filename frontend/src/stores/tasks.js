import { defineStore } from 'pinia';
import { getTasks, createTask as apiCreateTask } from '../api/tasks';

export const useTaskStore = defineStore('tasks', {
    state: () => ({
        tasks: [],
        total: 0,
        page: 1,
        limit: 10,
        filters: {
            status: '',
            priority: '',
            search: ''
        }
    }),
    actions: {
        async fetchTasks(params = {}) {
            const queryParams = {
                page: params.page || this.page,
                limit: params.limit || this.limit,
                ...(params.status || this.filters.status ? { status: params.status || this.filters.status } : {}),
                ...(params.priority || this.filters.priority ? { priority: params.priority || this.filters.priority } : {}),
                ...(params.search || this.filters.search ? { search: params.search || this.filters.search } : {}),
            };
            const res = await getTasks(queryParams);
            this.tasks = res.data.items || res.data;
            this.total = res.data.total || 0;
            return res.data;
        },
        async createTask(taskData) {
            const res = await apiCreateTask(taskData);
            return res.data;
        },
        setFilters(filters) {
            this.filters = { ...this.filters, ...filters };
            this.page = 1;
            this.fetchTasks();
        },
        setPage(page) {
            this.page = page;
            this.fetchTasks();
        }
    }
});