import { useDashboard } from "../hooks/useDashboard";
import { useTransactions } from "../hooks/useTransactions";
import SpendingSummary from "../components/SpendingSummary";
import CategoryChart from "../components/CategoryChart";
import TrendChart from "../components/TrendChart";
import TransactionTable from "../components/TransactionTable";

export default function DashboardPage() {
  const { data: dashboard, isLoading: dashLoading, error: dashError } = useDashboard();
  const { data: txnData, isLoading: txnLoading } = useTransactions();

  if (dashLoading || txnLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin h-8 w-8 border-4 border-primary-500 border-t-transparent rounded-full" />
      </div>
    );
  }

  if (dashError) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <p className="text-red-700">Failed to load dashboard data.</p>
      </div>
    );
  }

  if (!dashboard) return null;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-sm text-gray-500 mt-1">Your financial overview at a glance</p>
      </div>

      <SpendingSummary data={dashboard} />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <CategoryChart data={dashboard.category_breakdown} />
        <TrendChart data={dashboard.monthly_spending} />
      </div>

      <TransactionTable transactions={txnData?.transactions || []} />
    </div>
  );
}
