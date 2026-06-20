import Anthropic from "@anthropic-ai/sdk";
import { NextRequest, NextResponse } from "next/server";
import { matchInvoiceToPO, buildInvoiceFromResult } from "@/lib/agent";
import { ExtractionResult } from "@/lib/types";

const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

type ImageMediaType = "image/jpeg" | "image/png" | "image/gif" | "image/webp";

export async function POST(req: NextRequest) {
  try {
    const formData = await req.formData();
    const file = formData.get("invoice") as File | null;

    if (!file) {
      return NextResponse.json({ error: "No file provided" }, { status: 400 });
    }

    const bytes = await file.arrayBuffer();
    const base64 = Buffer.from(bytes).toString("base64");

    // Claude vision only supports image types — convert PDF to treat as PNG for demo
    const rawType = file.type;
    const mediaType: ImageMediaType = (
      rawType === "image/jpeg" ||
      rawType === "image/png" ||
      rawType === "image/gif" ||
      rawType === "image/webp"
        ? rawType
        : "image/png"
    ) as ImageMediaType;

    const message = await client.messages.create({
      model: "claude-opus-4-5",
      max_tokens: 1024,
      messages: [
        {
          role: "user",
          content: [
            {
              type: "image",
              source: {
                type: "base64",
                media_type: mediaType,
                data: base64,
              },
            },
            {
              type: "text",
              text: `Extract the following fields from this invoice and return ONLY a valid JSON object, no markdown, no explanation:
{
  "vendor": "vendor/company name",
  "invoiceNumber": "invoice number or ID",
  "amount": <total amount as number, no currency symbol>,
  "dueDate": "YYYY-MM-DD format",
  "lineItems": [
    { "description": "...", "quantity": <number>, "unitPrice": <number>, "total": <number> }
  ]
}

If a field is not found, use reasonable defaults: dueDate defaults to 30 days from today, amount to 0.`,
            },
          ],
        },
      ],
    });

    const text = message.content[0].type === "text" ? message.content[0].text : "";

    // Strip markdown code fences if Claude wraps the JSON
    const cleaned = text.trim().replace(/^```(?:json)?\n?/, "").replace(/\n?```$/, "");
    const extracted: ExtractionResult = JSON.parse(cleaned);

    const matchResult = matchInvoiceToPO(extracted);
    const id = `INV-${Date.now()}`;
    const invoice = buildInvoiceFromResult(matchResult, id);

    return NextResponse.json({ invoice });
  } catch (err) {
    console.error(err);
    return NextResponse.json({ error: "Extraction failed" }, { status: 500 });
  }
}
