// ─── Auth ────────────────────────────────────────────────────────────────────

export interface UserCreate {
  email: string;
  password: string;
}

export interface UserResponse {
  user_id: string;
  email: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

// ─── Transactions ────────────────────────────────────────────────────────────

export interface Transaction {
  transaction_id: string;
  date: string;
  description: string;
  amount: number;
  category: string;
  file_id?: string;
}

export interface TransactionListResponse {
  transactions: Transaction[];
  count: number;
}

// ─── Files ───────────────────────────────────────────────────────────────────

export type FileStatus = "pending" | "processing" | "completed" | "failed";

export interface FileUploadResponse {
  file_id: string;
  filename: string;
  status: FileStatus;
}

export interface FileStatusResponse {
  file_id: string;
  filename: string;
  status: FileStatus;
  transaction_count: number;
  error_message?: string;
  upload_date: string;
}

// ─── Dashboard ───────────────────────────────────────────────────────────────

export interface CategoryBreakdown {
  category: string;
  total: number;
  count: number;
  percentage: number;
}

export interface MonthlySpending {
  month: string;
  total: number;
  categories: CategoryBreakdown[];
}

export interface DashboardData {
  total_spending: number;
  transaction_count: number;
  monthly_spending: MonthlySpending[];
  category_breakdown: CategoryBreakdown[];
}
