"use client";

import { useApp } from "@/lib/store";
import { useState, useRef, useEffect } from "react";
import {
  Send,
  ArrowLeft,
  Bot,
  User,
  Sparkles,
  MessageCircle,
} from "lucide-react";

export default function ChatPage() {
  const { chatMessages, sendMessage, setPage, summary } = useApp();
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatMessages]);

  // Track typing indicator
  useEffect(() => {
    const lastMsg = chatMessages[chatMessages.length - 1];
    if (lastMsg?.role === "user") {
      setIsTyping(true);
    } else {
      setIsTyping(false);
    }
  }, [chatMessages]);

  const handleSend = () => {
    const trimmed = input.trim();
    if (!trimmed) return;
    sendMessage(trimmed);
    setInput("");
    inputRef.current?.focus();
  };

  const quickQuestions = [
    "What is an FD?",
    "Why are you recommending this?",
    "Can I save ₹5000 this month?",
    "Show my spending summary",
    "Why not keep money in savings?",
    "How much emergency fund do I need?",
  ];

  return (
    <div className="flex-1 flex flex-col h-screen animate-fade-up">
      {/* Header */}
      <div className="border-b border-border bg-surface/50 backdrop-blur-sm">
        <div className="max-w-4xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button
              onClick={() => setPage(summary ? "dashboard" : "landing")}
              className="p-2 rounded-lg hover:bg-surface-2 transition-colors"
            >
              <ArrowLeft className="w-5 h-5 text-muted" />
            </button>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-primary/15 flex items-center justify-center">
                <Bot className="w-5 h-5 text-primary" />
              </div>
              <div>
                <h2 className="font-semibold text-sm">AI Money Coach</h2>
                <div className="flex items-center gap-1.5 text-xs text-muted">
                  <div className="w-1.5 h-1.5 rounded-full bg-success animate-pulse-dot" />
                  Online
                </div>
              </div>
            </div>
          </div>
          {summary && (
            <button
              onClick={() => setPage("dashboard")}
              className="text-sm text-muted hover:text-foreground transition-colors"
            >
              Back to Dashboard
            </button>
          )}
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-4xl mx-auto px-6 py-6 space-y-6">
          {/* Empty state */}
          {chatMessages.length === 0 && (
            <div className="text-center py-12">
              <div className="w-16 h-16 mx-auto mb-5 rounded-2xl bg-primary/10 flex items-center justify-center">
                <MessageCircle className="w-7 h-7 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-2">
                Ask me anything about your money
              </h3>
              <p className="text-sm text-muted mb-8 max-w-md mx-auto">
                I can explain financial concepts, analyze your spending, and
                help you make better savings decisions.
              </p>

              {/* Quick questions */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 max-w-lg mx-auto">
                {quickQuestions.map((q) => (
                  <button
                    key={q}
                    onClick={() => sendMessage(q)}
                    className="text-left px-4 py-3 rounded-xl border border-border bg-surface hover:bg-surface-2 hover:border-border-light transition-all text-sm text-muted hover:text-foreground"
                  >
                    <Sparkles className="w-3.5 h-3.5 inline mr-2 text-primary" />
                    {q}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Chat messages */}
          {chatMessages.map((msg) => (
            <div
              key={msg.id}
              className={`flex gap-3 ${
                msg.role === "user" ? "justify-end" : "justify-start"
              }`}
            >
              {msg.role === "assistant" && (
                <div className="w-8 h-8 rounded-lg bg-primary/15 flex items-center justify-center shrink-0 mt-1">
                  <Bot className="w-4 h-4 text-primary" />
                </div>
              )}

              <div
                className={`max-w-[75%] rounded-2xl px-5 py-3.5 text-sm leading-relaxed
                  ${
                    msg.role === "user"
                      ? "bg-primary text-background rounded-br-md"
                      : "glass-card rounded-bl-md"
                  }`}
              >
                <div
                  className="prose prose-sm prose-invert max-w-none
                    [&_strong]:text-foreground [&_strong]:font-semibold
                    [&_h1]:text-lg [&_h2]:text-base [&_h3]:text-sm
                    [&_ul]:list-disc [&_ul]:pl-4 [&_ul]:space-y-1
                    [&_ol]:list-decimal [&_ol]:pl-4 [&_ol]:space-y-1
                    [&_p]:mb-2 [&_p:last-child]:mb-0
                    [&_table]:w-full [&_table]:text-xs
                    [&_th]:text-left [&_th]:pb-1 [&_th]:pr-4 [&_th]:border-b [&_th]:border-border
                    [&_td]:py-1 [&_td]:pr-4"
                  dangerouslySetInnerHTML={{
                    __html: formatMarkdown(msg.content),
                  }}
                />
              </div>

              {msg.role === "user" && (
                <div className="w-8 h-8 rounded-lg bg-surface-3 flex items-center justify-center shrink-0 mt-1">
                  <User className="w-4 h-4 text-muted" />
                </div>
              )}
            </div>
          ))}

          {/* Typing indicator */}
          {isTyping && (
            <div className="flex gap-3 items-start">
              <div className="w-8 h-8 rounded-lg bg-primary/15 flex items-center justify-center shrink-0">
                <Bot className="w-4 h-4 text-primary" />
              </div>
              <div className="glass-card rounded-2xl rounded-bl-md px-5 py-4">
                <div className="flex gap-1.5">
                  <div className="w-2 h-2 bg-muted rounded-full animate-bounce [animation-delay:0ms]" />
                  <div className="w-2 h-2 bg-muted rounded-full animate-bounce [animation-delay:150ms]" />
                  <div className="w-2 h-2 bg-muted rounded-full animate-bounce [animation-delay:300ms]" />
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input bar */}
      <div className="border-t border-border bg-surface/50 backdrop-blur-sm">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <div className="flex gap-3">
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
              placeholder="Ask about FDs, savings, or your spending..."
              className="flex-1 px-5 py-3 rounded-xl bg-surface-2 border border-border text-sm placeholder-muted focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/20 transition-all"
            />
            <button
              onClick={handleSend}
              disabled={!input.trim()}
              className="px-4 py-3 rounded-xl bg-primary text-background hover:bg-primary-dim disabled:opacity-40 disabled:cursor-not-allowed transition-all"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

/* Simple markdown-like formatter (no external deps) */
function formatMarkdown(text: string): string {
  return text
    // Bold
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    // Italic
    .replace(/\*(.*?)\*/g, "<em>$1</em>")
    // Headers
    .replace(/^### (.*$)/gm, "<h3>$1</h3>")
    .replace(/^## (.*$)/gm, "<h2>$1</h2>")
    .replace(/^# (.*$)/gm, "<h1>$1</h1>")
    // Table rows
    .replace(/\|(.+)\|/gm, (match) => {
      if (match.includes("---")) return "";
      const cells = match
        .split("|")
        .filter(Boolean)
        .map((c) => c.trim());
      const tag = match.includes("**") ? "th" : "td";
      return `<tr>${cells.map((c) => `<${tag}>${c}</${tag}>`).join("")}</tr>`;
    })
    // Unordered list items
    .replace(/^- (.*$)/gm, "<li>$1</li>")
    // Ordered list items
    .replace(/^\d+\. (.*$)/gm, "<li>$1</li>")
    // Wrap consecutive li in ul
    .replace(/((<li>.*<\/li>\n?)+)/g, "<ul>$1</ul>")
    // Wrap table rows
    .replace(/((<tr>.*<\/tr>\n?)+)/g, "<table>$1</table>")
    // Line breaks
    .replace(/\n\n/g, "<br/><br/>")
    .replace(/\n/g, "<br/>");
}
