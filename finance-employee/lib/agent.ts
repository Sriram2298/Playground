import { ExtractionResult, Invoice, AgentAction, InvoiceStatus } from "./types";
import { MOCK_POS } from "./mock-data";

const TOLERANCE = 0.05; // 5% variance allowed

export function matchInvoiceToPO(extracted: ExtractionResult): {
  status: InvoiceStatus;
  matchedPoId?: string;
  discrepancyReason?: string;
  agentActions: AgentAction[];
  amount: number;
  dueDate: string;
  vendor: string;
  invoiceNumber: string;
  lineItems: typeof extracted.lineItems;
} {
  const now = new Date().toISOString();
  const agentActions: AgentAction[] = [];

  // Fuzzy vendor match
  const po = MOCK_POS.find(
    (p) =>
      p.vendor.toLowerCase().includes(extracted.vendor.toLowerCase()) ||
      extracted.vendor.toLowerCase().includes(p.vendor.toLowerCase().split(" ")[0])
  );

  if (!po) {
    agentActions.push({
      timestamp: now,
      type: "flagged_discrepancy",
      description: `No matching PO found for vendor "${extracted.vendor}". Flagged for manual review.`,
      draftedEmail: `Subject: Unknown Vendor Invoice - Action Required\n\nAn invoice for $${extracted.amount.toLocaleString()} was received from "${extracted.vendor}" but no matching Purchase Order exists.\n\nPlease review and either create a PO or reject the invoice.\n\nZamp Finance Agent`,
    });
    return {
      status: "discrepancy",
      discrepancyReason: `No PO found for vendor: ${extracted.vendor}`,
      agentActions,
      ...extracted,
    };
  }

  const variance = Math.abs(extracted.amount - po.amount) / po.amount;
  const isOverdue = new Date(extracted.dueDate) < new Date();

  if (isOverdue) {
    agentActions.push({
      timestamp: now,
      type: "chaser_sent",
      description: `Invoice is past due. Chaser email drafted for ${extracted.vendor}.`,
      draftedEmail: `Subject: Overdue Invoice Reminder - ${extracted.invoiceNumber}\n\nDear ${extracted.vendor},\n\nInvoice ${extracted.invoiceNumber} for $${extracted.amount.toLocaleString()} was due on ${extracted.dueDate} and remains unpaid.\n\nPlease arrange payment at your earliest convenience.\n\nZamp Finance Agent`,
    });
    return {
      status: "overdue",
      matchedPoId: po.id,
      agentActions,
      ...extracted,
    };
  }

  if (variance > TOLERANCE) {
    const diff = extracted.amount - po.amount;
    agentActions.push({
      timestamp: now,
      type: "flagged_discrepancy",
      description: `Invoice amount $${extracted.amount.toLocaleString()} differs from PO ${po.id} ($${po.amount.toLocaleString()}) by ${(variance * 100).toFixed(1)}%. Flagged for approval.`,
      draftedEmail: `Subject: Invoice Discrepancy - ${extracted.invoiceNumber} requires approval\n\nHi,\n\nInvoice ${extracted.invoiceNumber} from ${extracted.vendor} has a discrepancy:\n\n• PO Amount: $${po.amount.toLocaleString()}\n• Invoice Amount: $${extracted.amount.toLocaleString()}\n• Difference: ${diff > 0 ? "+" : ""}$${diff.toLocaleString()} (${(variance * 100).toFixed(1)}%)\n\nPlease approve or reject this invoice.\n\nZamp Finance Agent`,
    });
    return {
      status: "discrepancy",
      matchedPoId: po.id,
      discrepancyReason: `Invoice amount differs from PO by ${(variance * 100).toFixed(1)}%`,
      agentActions,
      ...extracted,
    };
  }

  // Clean match
  agentActions.push({
    timestamp: now,
    type: "auto_approved",
    description: `Invoice matched ${po.id} within ${(variance * 100).toFixed(1)}% variance. Auto-approved.`,
    draftedEmail: `Subject: Payment Confirmation - ${extracted.invoiceNumber}\n\nDear ${extracted.vendor},\n\nThis confirms receipt and approval of invoice ${extracted.invoiceNumber} for $${extracted.amount.toLocaleString()}.\nPayment has been scheduled for ${extracted.dueDate}.\n\nZamp Finance Agent`,
  });
  agentActions.push({
    timestamp: now,
    type: "payment_scheduled",
    description: `Payment of $${extracted.amount.toLocaleString()} scheduled for ${extracted.dueDate}.`,
  });

  return {
    status: "matched",
    matchedPoId: po.id,
    agentActions,
    ...extracted,
  };
}

export function buildInvoiceFromResult(
  result: ReturnType<typeof matchInvoiceToPO>,
  id: string
): Invoice {
  return {
    id,
    vendor: result.vendor,
    invoiceNumber: result.invoiceNumber,
    amount: result.amount,
    dueDate: result.dueDate,
    receivedDate: new Date().toISOString().split("T")[0],
    lineItems: result.lineItems,
    status: result.status,
    matchedPoId: result.matchedPoId,
    discrepancyReason: result.discrepancyReason,
    agentActions: result.agentActions,
  };
}
