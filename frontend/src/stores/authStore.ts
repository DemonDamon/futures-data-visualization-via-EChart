import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import axios from 'axios';

interface User {
  id: string;
  username: string;
  email: string;
  created_at: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  checkAuth: () => Promise<void>;
}

const API_BASE_URL = 'http://localhost:8000/api';

// 配置axios默认设置
axios.defaults.baseURL = API_BASE_URL;

export const useAuthStore = create<AuthState>()(persist(
  (set, get) => ({
    user: null,
    token: null,
    isAuthenticated: false,
    isLoading: false,

    login: async (email: string, password: string) => {
      set({ isLoading: true });
      try {
        const response = await axios.post('/auth/login', {
          email,
          password
        });
        
        const { access_token, user } = response.data;
        
        // 设置axios默认header
        axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
        
        set({
          user,
          token: access_token,
          isAuthenticated: true,
          isLoading: false
        });
      } catch (error: any) {
        set({ isLoading: false });
        const message = error.response?.data?.detail || error.message || '登录失败';
        throw new Error(message);
      }
    },

    register: async (username: string, email: string, password: string) => {
      set({ isLoading: true });
      try {
        const response = await axios.post('/auth/register', {
          username,
          email,
          password
        });
        
        const { access_token, user } = response.data;
        
        // 设置axios默认header
        axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
        
        set({
          user,
          token: access_token,
          isAuthenticated: true,
          isLoading: false
        });
      } catch (error: any) {
        set({ isLoading: false });
        const message = error.response?.data?.detail || error.message || '注册失败';
        throw new Error(message);
      }
    },

    logout: () => {
      // 清除axios默认header
      delete axios.defaults.headers.common['Authorization'];
      
      set({
        user: null,
        token: null,
        isAuthenticated: false,
        isLoading: false
      });
    },

    checkAuth: async () => {
      const { token } = get();
      if (!token) {
        return;
      }
      
      set({ isLoading: true });
      try {
        // 设置axios默认header
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        
        const response = await axios.get('/auth/me');
        const user = response.data;
        
        set({
          user,
          isAuthenticated: true,
          isLoading: false
        });
      } catch (error) {
        // token无效，清除认证状态
        delete axios.defaults.headers.common['Authorization'];
        set({
          user: null,
          token: null,
          isAuthenticated: false,
          isLoading: false
        });
      }
    }
  }),
  {
    name: 'auth-storage',
    partialize: (state) => ({
      user: state.user,
      token: state.token,
      isAuthenticated: state.isAuthenticated
    })
  }
));

// 初始化时检查认证状态
if (typeof window !== 'undefined') {
  const { token } = useAuthStore.getState();
  if (token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    useAuthStore.getState().checkAuth();
  }
}