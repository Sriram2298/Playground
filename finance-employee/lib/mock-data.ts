import { Invoice, PurchaseOrder } from "./types";

export const MOCK_POS: PurchaseOrder[] = [
  {
    id: "PO-2024-001",
    vendor: "Acme Software Ltd",
    amount: 12500.00,
    dueDate: "2024-02-15",
    lineItems: [
      { description: "Enterprise License Q1", quantity: 1, unitPrice: 10000, total: 10000 },
      { description: "Support & Maintenance", quantity: 1, unitPrice: 2500, total: 2500 },
    ],
    status: "open",
  },
  {
    id: "PO-2024-002",
    vendor: "CloudHost Inc",
    amount: 4800.00,
    dueDate: "2024-02-20",
    lineItems: [
      { description: "Cloud Hosting Jan-Mar", quantity: 3, unitPrice: 1600, total: 4800 },
    ],
    status: "open",
  },
  {
    id: "PO-2024-003",
    vendor: "DataSync Corp",
    amount: 8200.00,
    dueDate: "2024-01-10",
    lineItems: [
      { description: "Data Pipeline Setup", quantity: 1, unitPrice: 6000, total: 6000 },
      { description: "Integration Hours", quantity: 8, unitPrice: 275, total: 2200 },
    ],
    status: "overdue",
  },
  {
    id: "PO-2024-004",
    vendor: "DesignStudio Pro",
    amount: 3500.00,
    dueDate: "2024-02-28",
    lineItems: [
      { description: "Brand Refresh Package", quantity: 1, unitPrice: 3500, total: 3500 },
    ],
    status: "open",
  },
  {
    id: "PO-2024-005",
    vendor: "SecureVault Systems",
    amount: 6750.00,
    dueDate: "2024-03-05",
    lineItems: [
      { description: "Security Audit", quantity: 1, unitPrice: 5000, total: 5000 },
      { description: "Penetration Testing", quantity: 1, unitPrice: 1750, total: 1750 },
    ],
    status: "open",
  },
];

export const MOCK_INVOICES: Invoice[] = [
  {
    id: "INV-001",
    vendor: "Acme Software Ltd",
    invoiceNumber: "ASL-9921",
    amount: 12500.00,
    dueDate: "2024-02-15",
    receivedDate: "2024-01-28",
    lineItems: [
      { description: "Enterprise License Q1", quantity: 1, unitPrice: 10000, total: 10000 },
      { description: "Support & Maintenance", quantity: 1, unitPrice: 2500, total: 2500 },
    ],
    status: "matched",
    matchedPoId: "PO-2024-001",
    agentActions: [
      {
        timestamp: "2024-01-28T09:12:00Z",
        type: "auto_approved",
        description: "Invoice matched PO-2024-001 within 0% variance. Payment scheduled for Feb 15.",
        draftedEmail: `Subject: Payment Confirmation - ASL-9921\n\nDear Acme Software Ltd,\n\nThis confirms receipt and approval of invoice ASL-9921 for $12,500.00.\nPayment has been scheduled for February 15, 2024.\n\nBest regards,\nFinance Agent`,
      },
      {
        timestamp: "2024-01-28T09:12:01Z",
        type: "payment_scheduled",
        description: "Payment of $12,500.00 queued for Feb 15, 2024.",
      },
    ],
  },
  {
    id: "INV-002",
    vendor: "CloudHost Inc",
    invoiceNumber: "CHI-4471",
    amount: 5200.00,
    dueDate: "2024-02-20",
    receivedDate: "2024-01-30",
    lineItems: [
      { description: "Cloud Hosting Jan-Mar", quantity: 3, unitPrice: 1600, total: 4800 },
      { description: "Bandwidth Overage", quantity: 1, unitPrice: 400, total: 400 },
    ],
    status: "discrepancy",
    matchedPoId: "PO-2024-002",
    discrepancyReason: "Invoice is $400 over PO amount. Bandwidth overage not in original PO scope.",
    agentActions: [
      {
        timestamp: "2024-01-30T11:05:00Z",
        type: "flagged_discrepancy",
        description: "Invoice CHI-4471 exceeds PO-2024-002 by $400 (8.3%). Flagged for CFO review.",
        draftedEmail: `Subject: Invoice Discrepancy - CHI-4471 requires approval\n\nHi,\n\nInvoice CHI-4471 from CloudHost Inc has a discrepancy:\n\n• PO Amount: $4,800.00\n• Invoice Amount: $5,200.00\n• Difference: +$400.00 (Bandwidth Overage)\n\nThis line item was not in the original PO scope. Please approve or reject.\n\nFinance Agent`,
      },
    ],
  },
  {
    id: "INV-003",
    vendor: "DataSync Corp",
    invoiceNumber: "DS-0088",
    amount: 8200.00,
    dueDate: "2024-01-10",
    receivedDate: "2023-12-28",
    lineItems: [
      { description: "Data Pipeline Setup", quantity: 1, unitPrice: 6000, total: 6000 },
      { description: "Integration Hours", quantity: 8, unitPrice: 275, total: 2200 },
    ],
    status: "overdue",
    matchedPoId: "PO-2024-003",
    agentActions: [
      {
        timestamp: "2024-01-11T08:00:00Z",
        type: "chaser_sent",
        description: "Invoice DS-0088 is 1 day overdue. Chaser sent to DataSync Corp.",
        draftedEmail: `Subject: Overdue Invoice Reminder - DS-0088\n\nDear DataSync Corp,\n\nOur records show invoice DS-0088 ($8,200.00) was due on January 10, 2024 and remains unpaid.\n\nPlease arrange payment at your earliest convenience or contact us to discuss.\n\nFinance Agent`,
      },
      {
        timestamp: "2024-01-18T08:00:00Z",
        type: "chaser_sent",
        description: "Second chaser sent. Invoice 8 days overdue. Escalating to account manager.",
        draftedEmail: `Subject: URGENT: Overdue Invoice DS-0088 - 8 Days Past Due\n\nDear DataSync Corp,\n\nThis is a second notice for invoice DS-0088 ($8,200.00), now 8 days overdue.\n\nPlease remit payment immediately or this will be escalated to your account manager.\n\nFinance Agent`,
      },
    ],
  },
  {
    id: "INV-004",
    vendor: "DesignStudio Pro",
    invoiceNumber: "DSP-2201",
    amount: 3500.00,
    dueDate: "2024-02-28",
    receivedDate: "2024-02-01",
    lineItems: [
      { description: "Brand Refresh Package", quantity: 1, unitPrice: 3500, total: 3500 },
    ],
    status: "matched",
    matchedPoId: "PO-2024-004",
    agentActions: [
      {
        timestamp: "2024-02-01T14:22:00Z",
        type: "auto_approved",
        description: "Invoice matched PO-2024-004 exactly. Payment scheduled for Feb 28.",
      },
      {
        timestamp: "2024-02-01T14:22:01Z",
        type: "payment_scheduled",
        description: "Payment of $3,500.00 queued for Feb 28, 2024.",
      },
    ],
  },
];
