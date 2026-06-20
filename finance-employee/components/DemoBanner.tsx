export default function DemoBanner() {
  return (
    <div className="bg-gray-900 text-gray-300 text-xs px-4 py-2 flex items-center gap-6 flex-wrap">
      <span className="font-semibold text-white">DEMO MODE</span>
      <span>• Emails drafted, not sent — connect Gmail to enable</span>
      <span>• Payments simulated — connect your ERP to execute</span>
      <span>• State resets on refresh — no persistent DB in demo</span>
      <span>• Invoice extraction via Claude Vision</span>
    </div>
  );
}
