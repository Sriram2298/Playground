import { InvoiceStatus } from "@/lib/types";

const CONFIG: Record<InvoiceStatus, { label: string; classes: string }> = {
  matched: { label: "Auto-Approved", classes: "bg-emerald-100 text-emerald-700" },
  discrepancy: { label: "Needs Review", classes: "bg-amber-100 text-amber-700" },
  overdue: { label: "Overdue", classes: "bg-red-100 text-red-700" },
  processing: { label: "Processing", classes: "bg-blue-100 text-blue-700" },
  paid: { label: "Paid", classes: "bg-gray-100 text-gray-600" },
};

export default function StatusBadge({ status }: { status: InvoiceStatus }) {
  const { label, classes } = CONFIG[status];
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${classes}`}>
      {label}
    </span>
  );
}
