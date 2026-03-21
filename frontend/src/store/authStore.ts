import { create } from "zustand";

interface AuthState {
  token: string | null;
  isAuthenticated: boolean;
  login: (token: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: localStorage.getItem("fintrack_token"),
  isAuthenticated: !!localStorage.getItem("fintrack_token"),

  login: (token: string) => {
    localStorage.setItem("fintrack_token", token);
    set({ token, isAuthenticated: true });
  },

  logout: () => {
    localStorage.removeItem("fintrack_token");
    set({ token: null, isAuthenticated: false });
  },
}));
