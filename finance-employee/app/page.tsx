import Link from "next/link";
import { MOCK_INVOICES } from "@/lib/mock-data";
import InvoiceCard from "@/components/InvoiceCard";
import StatusBadge from "@/components/StatusBadge";

export default function Dashboard() {
  const total = MOCK_INVOICES.reduce((s, i) => s + i.amount, 0);
  const matched = MOCK_INVOICES.filter((i) => i.status === "matched").length;
  const discrepancies = MOCK_INVOICES.filter((i) => i.status === "discrepancy").length;
  const overdue = MOCK_INVOICES.filter((i) => i.status === "overdue").length;
  const autoHandled = MOCK_INVOICES.filter((i) => i.status === "matched" || i.status === "paid").length;
  const autoRate = Math.round((autoHandled / MOCK_INVOICES.length) * 100);

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-gray-900">AP/AR Dashboard</h1>
        <p className="text-sm text-gray-500 mt-1">
          Your digital finance employee — running autonomously.
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <StatCard label="Total Invoices" value={`$${total.toLocaleString()}`} sub={`${MOCK_INVOICES.length} invoices`} />
        <StatCard label="Auto-Approved" value={`${matched}`} sub="No human needed" color="emerald" />
        <StatCard label="Need Review" value={`${discrepancies}`} sub="Flagged by agent" color="amber" />
        <StatCard label="Overdue" value={`${overdue}`} sub="Chasers sent" color="red" />
      </div>

      {/* Agent summary */}
      <div className="bg-gray-900 text-white rounded-xl p-5 mb-8 flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-400">Agent autonomy rate</p>
          <p className="text-3xl font-bold mt-1">{autoRate}%</p>
          <p className="text-sm text-gray-400 mt-1">
            {autoHandled} of {MOCK_INVOICES.length} invoices handled without human input
          </p>
        </div>
        <div className="text-right">
          <p className="text-sm text-gray-400">Next action</p>
          <p className="text-sm text-white mt-1 font-medium">Chaser #2 due for DataSync Corp</p>
          <p className="text-xs text-gray-500 mt-0.5">in 2 days</p>
        </div>
      </div>

      {/* Invoice list */}
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-sm font-semibold text-gray-700 uppercase tracking-wide">Invoices</h2>
        <Link
          href="/upload"
          className="text-sm bg-gray-900 text-white px-4 py-1.5 rounded-lg hover:bg-gray-700 transition-colors"
        >
          + Process Invoice
        </Link>
      </div>

      <div className="space-y-3">
        {MOCK_INVOICES.map((invoice) => (
          <InvoiceCard key={invoice.id} invoice={invoice} />
        ))}
      </div>
    </div>
  );
}

function StatCard({
  label,
  value,
  sub,
  color,
}: {
  label: string;
  value: string;
  sub: string;
  color?: "emerald" | "amber" | "red";
}) {
  const border = color === "emerald"
    ? "border-emerald-200"
    : color === "amber"
    ? "border-amber-200"
    : color === "red"
    ? "border-red-200"
    : "border-gray-200";

  return (
    <div className={`bg-white border ${border} rounded-xl p-4`}>
      <p className="text-xs text-gray-500">{label}</p>
      <p className="text-2xl font-bold text-gray-900 mt-1">{value}</p>
      <p className="text-xs text-gray-400 mt-0.5">{sub}</p>
    </div>
  );
}
