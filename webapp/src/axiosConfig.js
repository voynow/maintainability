import axios from 'axios';
import supabase from './supabaseClient';

const api = axios.create({
    baseURL: process.env.REACT_APP_API_URL,
});

api.interceptors.request.use(async (config) => {
    const session = supabase.auth.session();
    if (session) {
        config.headers.Authorization = `Bearer ${session.access_token}`;
    }
    return config;
});

export default api;
