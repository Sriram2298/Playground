"use client";
import { Invoice } from "@/lib/types";
import { useState } from "react";
import StatusBadge from "./StatusBadge";
import ActionLog from "./ActionLog";

export default function InvoiceCard({ invoice }: { invoice: Invoice }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full text-left px-5 py-4 hover:bg-gray-50 transition-colors"
      >
        <div className="flex items-center justify-between gap-4">
          <div className="flex items-center gap-3 min-w-0">
            <div className="w-9 h-9 rounded-lg bg-gray-100 flex items-center justify-center text-sm font-bold text-gray-500 shrink-0">
              {invoice.vendor.charAt(0)}
            </div>
            <div className="min-w-0">
              <p className="font-medium text-gray-900 truncate">{invoice.vendor}</p>
              <p className="text-xs text-gray-400">{invoice.invoiceNumber}</p>
            </div>
          </div>
          <div className="flex items-center gap-4 shrink-0">
            <div className="text-right">
              <p className="font-semibold text-gray-900">${invoice.amount.toLocaleString()}</p>
              <p className="text-xs text-gray-400">Due {invoice.dueDate}</p>
            </div>
            <StatusBadge status={invoice.status} />
            <span className="text-gray-400 text-sm">{expanded ? "▲" : "▼"}</span>
          </div>
        </div>
      </button>

      {expanded && (
        <div className="border-t border-gray-100 px-5 py-4 space-y-4 bg-gray-50/50">
          {invoice.discrepancyReason && (
            <div className="bg-amber-50 border border-amber-200 rounded-lg px-3 py-2 text-sm text-amber-700">
              <span className="font-medium">Discrepancy: </span>{invoice.discrepancyReason}
            </div>
          )}

          {invoice.matchedPoId && (
            <p className="text-xs text-gray-500">
              Matched to: <span className="font-mono font-medium text-gray-700">{invoice.matchedPoId}</span>
            </p>
          )}

          <div>
            <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Line Items</p>
            <table className="w-full text-sm">
              <thead>
                <tr className="text-xs text-gray-400 border-b border-gray-200">
                  <th className="text-left pb-1">Description</th>
                  <th className="text-right pb-1">Qty</th>
                  <th className="text-right pb-1">Unit</th>
                  <th className="text-right pb-1">Total</th>
                </tr>
              </thead>
              <tbody>
                {invoice.lineItems.map((item, i) => (
                  <tr key={i} className="border-b border-gray-100 last:border-0">
                    <td className="py-1.5 text-gray-700">{item.description}</td>
                    <td className="py-1.5 text-right text-gray-500">{item.quantity}</td>
                    <td className="py-1.5 text-right text-gray-500">${item.unitPrice.toLocaleString()}</td>
                    <td className="py-1.5 text-right font-medium">${item.total.toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div>
            <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Agent Activity</p>
            <ActionLog actions={invoice.agentActions} />
          </div>
        </div>
      )}
    </div>
  );
}
