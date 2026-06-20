export type InvoiceStatus = "matched" | "discrepancy" | "overdue" | "processing" | "paid";

export type ActionType =
  | "auto_approved"
  | "flagged_discrepancy"
  | "chaser_sent"
  | "payment_scheduled";

export interface LineItem {
  description: string;
  quantity: number;
  unitPrice: number;
  total: number;
}

export interface PurchaseOrder {
  id: string;
  vendor: string;
  amount: number;
  dueDate: string;
  lineItems: LineItem[];
  status: "open" | "paid" | "overdue";
}

export interface Invoice {
  id: string;
  vendor: string;
  invoiceNumber: string;
  amount: number;
  dueDate: string;
  receivedDate: string;
  lineItems: LineItem[];
  status: InvoiceStatus;
  matchedPoId?: string;
  discrepancyReason?: string;
  agentActions: AgentAction[];
}

export interface AgentAction {
  timestamp: string;
  type: ActionType;
  description: string;
  draftedEmail?: string;
}

export interface ExtractionResult {
  vendor: string;
  invoiceNumber: string;
  amount: number;
  dueDate: string;
  lineItems: LineItem[];
}
