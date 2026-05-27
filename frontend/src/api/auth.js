import api from './index';

export const login = (data) => {
    const formData = new URLSearchParams();
    formData.append('username', data.email);
    formData.append('password', data.password);
    return api.post('/auth/login', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });
};
export const register = (data) => api.post('/auth/register', data);
export const fetchMe = () => api.get('/auth/me');
