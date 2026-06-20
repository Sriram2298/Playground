"use client";

const CONNECTORS = [
  {
    name: "Gmail",
    description: "Ingest invoices directly from email. Agent monitors inbox and processes attachments automatically.",
    icon: "✉",
    category: "Email",
    impact: "Eliminates manual upload",
  },
  {
    name: "QuickBooks",
    description: "Sync approved invoices and execute real payments. Close the loop without touching your accounting software.",
    icon: "📊",
    category: "Accounting",
    impact: "Real payment execution",
  },
  {
    name: "Stripe",
    description: "Pull payment history and reconcile automatically. Detects discrepancies across your payment processor.",
    icon: "⚡",
    category: "Payments",
    impact: "Auto-reconciliation",
  },
  {
    name: "Slack",
    description: "Agent sends escalations and approval requests directly to Slack instead of email drafts.",
    icon: "💬",
    category: "Notifications",
    impact: "Faster human decisions",
  },
  {
    name: "Google Drive",
    description: "Watch a shared folder for invoice uploads. Any PDF dropped in gets processed immediately.",
    icon: "📁",
    category: "Storage",
    impact: "Zero-friction ingestion",
  },
  {
    name: "SAP / NetSuite",
    description: "Push approved invoices and payment schedules into your ERP. Full audit trail maintained.",
    icon: "🏢",
    category: "ERP",
    impact: "End-to-end automation",
  },
];

export default function ConnectorsPage() {
  return (
    <div className="p-8 max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-gray-900">Connectors</h1>
        <p className="text-sm text-gray-500 mt-1">
          Connect your tools to unlock full autonomous operation.
        </p>
      </div>

      {/* Demo notice */}
      <div className="bg-amber-50 border border-amber-200 rounded-xl px-4 py-3 text-sm text-amber-700 mb-8">
        <span className="font-semibold">Demo limitation:</span> Connectors are not live in this demo. In production, each connector removes a step that currently requires manual input.
      </div>

      {/* What connectors unlock */}
      <div className="bg-gray-900 text-white rounded-xl p-5 mb-8">
        <p className="text-sm text-gray-400 mb-3">Without connectors vs. with connectors</p>
        <div className="grid grid-cols-2 gap-6 text-sm">
          <div>
            <p className="text-gray-400 text-xs uppercase tracking-wide mb-2">Demo (now)</p>
            <ul className="space-y-1.5 text-gray-300">
              <li>→ Manual invoice upload</li>
              <li>→ Emails drafted, not sent</li>
              <li>→ Payments simulated</li>
              <li>→ No ERP sync</li>
            </ul>
          </div>
          <div>
            <p className="text-gray-400 text-xs uppercase tracking-wide mb-2">Production (connected)</p>
            <ul className="space-y-1.5 text-white">
              <li>✓ Auto-ingests from Gmail / Drive</li>
              <li>✓ Sends real approval/chaser emails</li>
              <li>✓ Executes payments via QuickBooks</li>
              <li>✓ Full ERP sync + audit trail</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Connector cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {CONNECTORS.map((c) => (
          <div key={c.name} className="bg-white border border-gray-200 rounded-xl p-5 flex items-start gap-4">
            <div className="w-10 h-10 rounded-lg bg-gray-100 flex items-center justify-center text-xl shrink-0">
              {c.icon}
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between gap-2">
                <div>
                  <p className="font-medium text-gray-900 text-sm">{c.name}</p>
                  <p className="text-xs text-gray-400">{c.category}</p>
                </div>
                <button
                  disabled
                  className="shrink-0 text-xs px-3 py-1.5 rounded-lg bg-gray-100 text-gray-400 cursor-not-allowed"
                  title="Not available in demo"
                >
                  Connect
                </button>
              </div>
              <p className="text-xs text-gray-500 mt-2">{c.description}</p>
              <p className="text-xs text-emerald-600 mt-1.5 font-medium">↑ {c.impact}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
