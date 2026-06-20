"use client";
import { useState, useRef } from "react";
import { Invoice } from "@/lib/types";
import InvoiceCard from "@/components/InvoiceCard";

type Stage = "idle" | "uploading" | "extracting" | "matching" | "done" | "error";

const STAGE_LABELS: Record<Stage, string> = {
  idle: "",
  uploading: "Uploading invoice...",
  extracting: "Extracting data with Claude Vision...",
  matching: "Matching to PO database...",
  done: "Done",
  error: "Something went wrong",
};

export default function UploadPage() {
  const [stage, setStage] = useState<Stage>("idle");
  const [result, setResult] = useState<Invoice | null>(null);
  const [dragOver, setDragOver] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  async function processFile(file: File) {
    setResult(null);
    setStage("uploading");

    const form = new FormData();
    form.append("invoice", file);

    setStage("extracting");
    const res = await fetch("/api/extract-invoice", { method: "POST", body: form });

    setStage("matching");
    await new Promise((r) => setTimeout(r, 600)); // small delay so matching step is visible

    if (!res.ok) {
      setStage("error");
      return;
    }

    const data = await res.json();
    setResult(data.invoice);
    setStage("done");
  }

  function handleFile(file: File) {
    if (!file.type.startsWith("image/") && file.type !== "application/pdf") {
      alert("Please upload an image or PDF invoice.");
      return;
    }
    processFile(file);
  }

  return (
    <div className="p-8 max-w-3xl mx-auto">
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-gray-900">Process Invoice</h1>
        <p className="text-sm text-gray-500 mt-1">
          Upload an invoice — the agent extracts, matches, and acts autonomously.
        </p>
      </div>

      {/* Upload zone */}
      <div
        onClick={() => stage === "idle" && inputRef.current?.click()}
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDragOver(false);
          const file = e.dataTransfer.files[0];
          if (file) handleFile(file);
        }}
        className={`border-2 border-dashed rounded-xl p-12 text-center transition-colors ${
          dragOver
            ? "border-gray-400 bg-gray-100"
            : stage === "idle"
            ? "border-gray-300 bg-white cursor-pointer hover:border-gray-400 hover:bg-gray-50"
            : "border-gray-200 bg-gray-50"
        }`}
      >
        <input
          ref={inputRef}
          type="file"
          accept="image/*,application/pdf"
          className="hidden"
          onChange={(e) => { const f = e.target.files?.[0]; if (f) handleFile(f); }}
        />

        {stage === "idle" && (
          <>
            <div className="text-4xl mb-3">📄</div>
            <p className="text-gray-700 font-medium">Drop invoice here or click to upload</p>
            <p className="text-sm text-gray-400 mt-1">PNG, JPG, PDF supported</p>
          </>
        )}

        {(stage === "uploading" || stage === "extracting" || stage === "matching") && (
          <div className="space-y-4">
            <div className="flex justify-center">
              <div className="w-8 h-8 border-2 border-gray-900 border-t-transparent rounded-full animate-spin" />
            </div>
            <p className="text-gray-700 font-medium">{STAGE_LABELS[stage]}</p>
            <div className="flex justify-center gap-2">
              {(["uploading", "extracting", "matching"] as Stage[]).map((s) => (
                <div
                  key={s}
                  className={`h-1.5 w-16 rounded-full transition-colors ${
                    ["uploading", "extracting", "matching"].indexOf(stage) >=
                    ["uploading", "extracting", "matching"].indexOf(s)
                      ? "bg-gray-900"
                      : "bg-gray-200"
                  }`}
                />
              ))}
            </div>
          </div>
        )}

        {stage === "error" && (
          <>
            <div className="text-4xl mb-3">⚠️</div>
            <p className="text-gray-700 font-medium">Extraction failed</p>
            <button
              onClick={() => setStage("idle")}
              className="mt-3 text-sm text-gray-500 underline"
            >
              Try again
            </button>
          </>
        )}

        {stage === "done" && !result && (
          <p className="text-gray-500">No result returned.</p>
        )}
      </div>

      {/* Agent reasoning */}
      {stage === "done" && result && (
        <div className="mt-6 space-y-4">
          <div className="bg-emerald-50 border border-emerald-200 rounded-xl px-4 py-3 text-sm text-emerald-700">
            Agent processed this invoice in under 3 seconds. No human needed.{" "}
            <button
              onClick={() => { setStage("idle"); setResult(null); }}
              className="underline ml-1"
            >
              Process another
            </button>
          </div>
          <InvoiceCard invoice={result} />
        </div>
      )}

      {/* How it works */}
      {stage === "idle" && (
        <div className="mt-8 grid grid-cols-3 gap-4">
          {[
            { step: "1", title: "Extract", desc: "Claude Vision pulls vendor, amount, line items, due date from the invoice." },
            { step: "2", title: "Match", desc: "Agent fuzzy-matches to your PO database and checks for discrepancies." },
            { step: "3", title: "Act", desc: "Auto-approve, flag for review, or send a chaser — all without human input." },
          ].map(({ step, title, desc }) => (
            <div key={step} className="bg-white border border-gray-200 rounded-xl p-4">
              <div className="w-6 h-6 rounded-full bg-gray-900 text-white text-xs flex items-center justify-center font-bold mb-2">
                {step}
              </div>
              <p className="font-medium text-sm text-gray-900">{title}</p>
              <p className="text-xs text-gray-500 mt-1">{desc}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
