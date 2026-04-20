"use client";

import { useApp } from "@/lib/store";
import { useRef, useState, DragEvent } from "react";
import {
  Upload,
  FileSpreadsheet,
  Sparkles,
  TrendingUp,
  Shield,
  ArrowRight,
  Database,
} from "lucide-react";

export default function LandingPage() {
  const { loadSampleData, uploadCSV } = useApp();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleFileUpload = (file: File) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const text = e.target?.result as string;
      if (text) uploadCSV(text);
    };
    reader.readAsText(file);
  };

  const handleDrop = (e: DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (file && (file.name.endsWith(".csv") || file.type === "text/csv")) {
      handleFileUpload(file);
    }
  };

  const handleDragOver = (e: DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  return (
    <div className="flex-1 flex flex-col">
      {/* Hero */}
      <div className="relative overflow-hidden">
        {/* Background glow */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[500px] rounded-full bg-primary/5 blur-[120px] pointer-events-none" />
        <div className="absolute top-20 right-1/4 w-[400px] h-[300px] rounded-full bg-accent/5 blur-[100px] pointer-events-none" />

        <div className="relative max-w-6xl mx-auto px-6 pt-16 pb-12">
          {/* Nav */}
          <nav className="flex items-center justify-between mb-20">
            <div className="flex items-center gap-2.5">
              <div className="w-9 h-9 rounded-xl bg-primary/20 flex items-center justify-center">
                <TrendingUp className="w-5 h-5 text-primary" />
              </div>
              <span className="text-lg font-bold tracking-tight">SaveSmart</span>
            </div>
            <div className="flex items-center gap-2 text-sm text-muted">
              <span>Powered by</span>
              <span className="font-semibold text-foreground flex items-center gap-1">
                <Shield className="w-3.5 h-3.5 text-primary" />
                Blostem
              </span>
            </div>
          </nav>

          {/* Main hero */}
          <div className="text-center max-w-3xl mx-auto mb-16">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-surface-2 border border-border text-sm text-muted mb-6">
              <Sparkles className="w-4 h-4 text-primary" />
              <span>AI-powered money guidance</span>
            </div>

            <h1 className="text-5xl sm:text-6xl font-extrabold tracking-tight leading-[1.08] mb-6">
              Understand your money.
              <br />
              <span className="text-primary">Grow it smarter.</span>
            </h1>

            <p className="text-lg text-muted leading-relaxed max-w-2xl mx-auto mb-10">
              Upload your bank statement, see where your money goes, and get a
              personalized fixed deposit recommendation — explained in plain
              English, ready to book.
            </p>

            {/* Feature pills */}
            <div className="flex flex-wrap justify-center gap-3 mb-12">
              {[
                { icon: "📊", text: "Spend analysis" },
                { icon: "🎯", text: "Safe-to-save calc" },
                { icon: "🏦", text: "FD recommendation" },
                { icon: "🤖", text: "AI explainer" },
                { icon: "✅", text: "One-click booking" },
              ].map((f) => (
                <span
                  key={f.text}
                  className="px-3.5 py-1.5 rounded-full bg-surface border border-border text-sm"
                >
                  {f.icon} {f.text}
                </span>
              ))}
            </div>
          </div>

          {/* Upload section */}
          <div className="max-w-2xl mx-auto">
            <div
              onDrop={handleDrop}
              onDragOver={handleDragOver}
              onDragLeave={() => setIsDragging(false)}
              className={`relative rounded-2xl border-2 border-dashed p-10 text-center transition-all duration-300 cursor-pointer group
                ${
                  isDragging
                    ? "border-primary bg-primary/5 scale-[1.01]"
                    : "border-border hover:border-primary/40 hover:bg-surface/50"
                }`}
              onClick={() => fileInputRef.current?.click()}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".csv"
                className="hidden"
                onChange={(e) => {
                  const file = e.target.files?.[0];
                  if (file) handleFileUpload(file);
                }}
              />

              <div className="w-16 h-16 mx-auto mb-5 rounded-2xl bg-primary/10 flex items-center justify-center group-hover:bg-primary/15 transition-colors">
                <Upload className="w-7 h-7 text-primary" />
              </div>

              <h3 className="text-xl font-semibold mb-2">
                Upload your bank statement
              </h3>
              <p className="text-muted text-sm mb-6">
                Drag & drop a CSV file here, or click to browse
              </p>

              <div className="flex items-center justify-center gap-2 text-xs text-muted">
                <FileSpreadsheet className="w-3.5 h-3.5" />
                <span>Supports CSV format • Columns: date, description, amount</span>
              </div>
            </div>

            {/* Divider */}
            <div className="flex items-center gap-4 my-6">
              <div className="flex-1 h-px bg-border" />
              <span className="text-xs text-muted font-medium uppercase tracking-widest">
                or try instantly
              </span>
              <div className="flex-1 h-px bg-border" />
            </div>

            {/* Sample data button */}
            <button
              onClick={loadSampleData}
              className="w-full py-4 rounded-xl bg-primary text-background font-semibold text-base flex items-center justify-center gap-3 hover:bg-primary-dim transition-colors active:scale-[0.99]"
            >
              <Database className="w-5 h-5" />
              Load sample data & explore
              <ArrowRight className="w-5 h-5" />
            </button>

            <p className="text-center text-xs text-muted mt-3">
              Pre-loaded with 30+ realistic transactions • Takes 2 seconds
            </p>
          </div>
        </div>
      </div>

      {/* How it works */}
      <div className="max-w-6xl mx-auto px-6 py-16">
        <h2 className="text-2xl font-bold text-center mb-10">
          How it works
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {[
            {
              step: "01",
              title: "Upload transactions",
              desc: "CSV from your bank or enter manually",
              color: "text-primary",
            },
            {
              step: "02",
              title: "See your spending",
              desc: "Auto-categorized with insights & charts",
              color: "text-accent",
            },
            {
              step: "03",
              title: "Get FD recommendation",
              desc: "Personalized to your cash flow pattern",
              color: "text-[#8b5cf6]",
            },
            {
              step: "04",
              title: "Book with Blostem",
              desc: "Simple handoff to secure FD booking",
              color: "text-[#ec4899]",
            },
          ].map((item) => (
            <div
              key={item.step}
              className="glass-card p-6 hover:border-border-light transition-colors group"
            >
              <span className={`text-4xl font-black ${item.color} opacity-30 group-hover:opacity-50 transition-opacity`}>
                {item.step}
              </span>
              <h3 className="font-semibold mt-3 mb-1.5">{item.title}</h3>
              <p className="text-sm text-muted leading-relaxed">{item.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
