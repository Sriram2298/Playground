"use client";
import { AgentAction, ActionType } from "@/lib/types";
import { useState } from "react";

const ACTION_ICONS: Record<ActionType, string> = {
  auto_approved: "✓",
  flagged_discrepancy: "⚠",
  chaser_sent: "↗",
  payment_scheduled: "⏱",
};

const ACTION_COLORS: Record<ActionType, string> = {
  auto_approved: "text-emerald-600 bg-emerald-50 border-emerald-200",
  flagged_discrepancy: "text-amber-600 bg-amber-50 border-amber-200",
  chaser_sent: "text-blue-600 bg-blue-50 border-blue-200",
  payment_scheduled: "text-purple-600 bg-purple-50 border-purple-200",
};

export default function ActionLog({ actions }: { actions: AgentAction[] }) {
  const [expandedEmail, setExpandedEmail] = useState<number | null>(null);

  return (
    <div className="space-y-3">
      {actions.map((action, i) => (
        <div key={i} className={`border rounded-lg p-3 ${ACTION_COLORS[action.type]}`}>
          <div className="flex items-start gap-2">
            <span className="text-sm font-bold mt-0.5">{ACTION_ICONS[action.type]}</span>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium">{action.description}</p>
              <p className="text-xs opacity-60 mt-0.5">
                {new Date(action.timestamp).toLocaleString()}
              </p>
              {action.draftedEmail && (
                <button
                  onClick={() => setExpandedEmail(expandedEmail === i ? null : i)}
                  className="mt-2 text-xs underline opacity-70 hover:opacity-100"
                >
                  {expandedEmail === i ? "Hide drafted email" : "View drafted email"}
                </button>
              )}
              {expandedEmail === i && action.draftedEmail && (
                <pre className="mt-2 text-xs bg-white/60 rounded p-2 whitespace-pre-wrap font-mono border border-current/20">
                  {action.draftedEmail}
                </pre>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
