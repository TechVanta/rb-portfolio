import client from "./client";
import type {
  DashboardData,
  FileStatusResponse,
  FileUploadResponse,
  TokenResponse,
  TransactionListResponse,
  UserResponse,
} from "../types";

// ─── Auth ────────────────────────────────────────────────────────────────────

export const authApi = {
  signup: (email: string, password: string) =>
    client.post<UserResponse>("/auth/signup", { email, password }),

  login: (email: string, password: string) =>
    client.post<TokenResponse>("/auth/login", { email, password }),
};

// ─── Files ───────────────────────────────────────────────────────────────────

export const filesApi = {
  upload: (file: File) => {
    const form = new FormData();
    form.append("file", file);
    return client.post<FileUploadResponse>("/files/upload", form, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },

  process: (fileId: string) =>
    client.post<FileStatusResponse>(`/files/${fileId}/process`),

  getStatus: (fileId: string) =>
    client.get<FileStatusResponse>(`/files/${fileId}/status`),
};

// ─── Transactions ────────────────────────────────────────────────────────────

export const transactionsApi = {
  list: () => client.get<TransactionListResponse>("/transactions"),
};

// ─── Dashboard ───────────────────────────────────────────────────────────────

export const dashboardApi = {
  get: () => client.get<DashboardData>("/dashboard"),
};
