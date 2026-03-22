import type { DashboardData } from "../types";

interface Props {
  data: DashboardData;
}

export default function SpendingSummary({ data }: Props) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <p className="text-sm text-gray-500">Total Spending</p>
        <p className="text-3xl font-bold text-gray-900 mt-1">
          ${data.total_spending.toLocaleString("en-US", { minimumFractionDigits: 2 })}
        </p>
      </div>
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <p className="text-sm text-gray-500">Transactions</p>
        <p className="text-3xl font-bold text-gray-900 mt-1">
          {data.transaction_count}
        </p>
      </div>
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <p className="text-sm text-gray-500">Categories</p>
        <p className="text-3xl font-bold text-gray-900 mt-1">
          {data.category_breakdown.length}
        </p>
      </div>
    </div>
  );
}
