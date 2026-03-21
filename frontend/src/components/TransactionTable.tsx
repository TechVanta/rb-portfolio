import type { Transaction } from "../types";

interface Props {
  transactions: Transaction[];
}

const CATEGORY_COLORS: Record<string, string> = {
  Food: "bg-orange-100 text-orange-700",
  Travel: "bg-blue-100 text-blue-700",
  Groceries: "bg-green-100 text-green-700",
  Bills: "bg-red-100 text-red-700",
  Shopping: "bg-purple-100 text-purple-700",
  Entertainment: "bg-pink-100 text-pink-700",
  Healthcare: "bg-teal-100 text-teal-700",
  Education: "bg-indigo-100 text-indigo-700",
  Transportation: "bg-yellow-100 text-yellow-700",
  Other: "bg-gray-100 text-gray-700",
};

export default function TransactionTable({ transactions }: Props) {
  if (transactions.length === 0) {
    return (
      <div className="bg-white rounded-xl border border-gray-200 p-8 text-center">
        <p className="text-gray-400">No transactions yet. Upload a statement to get started.</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900">Recent Transactions</h3>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-3">
                Date
              </th>
              <th className="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-3">
                Description
              </th>
              <th className="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-3">
                Category
              </th>
              <th className="text-right text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-3">
                Amount
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {transactions.map((txn) => (
              <tr key={txn.transaction_id} className="hover:bg-gray-50 transition-colors">
                <td className="px-6 py-4 text-sm text-gray-600 whitespace-nowrap">
                  {txn.date}
                </td>
                <td className="px-6 py-4 text-sm text-gray-900 max-w-xs truncate">
                  {txn.description}
                </td>
                <td className="px-6 py-4">
                  <span
                    className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      CATEGORY_COLORS[txn.category] || CATEGORY_COLORS.Other
                    }`}
                  >
                    {txn.category}
                  </span>
                </td>
                <td className="px-6 py-4 text-sm text-right font-medium whitespace-nowrap">
                  <span className={txn.amount < 0 ? "text-green-600" : "text-gray-900"}>
                    {txn.amount < 0 ? "+" : ""}$
                    {Math.abs(txn.amount).toLocaleString("en-US", {
                      minimumFractionDigits: 2,
                    })}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
