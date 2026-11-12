"use client";
import { useState } from "react";

export function downloadCsv(filename: string, rows: (string | number)[][]) {
  const esc = (v: string | number) => {
    const s = String(v ?? "");
    return /[",\n;]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
  };
  const blob = new Blob(["﻿" + rows.map((r) => r.map(esc).join(",")).join("\n")], { type: "text/csv;charset=utf-8" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = filename;
  a.click();
  URL.revokeObjectURL(a.href);
}

export function ShareButton() {
  const [done, setDone] = useState(false);
  return (
    <button
      className="btn"
      onClick={async () => {
        try {
          await navigator.clipboard.writeText(window.location.href);
          setDone(true);
          setTimeout(() => setDone(false), 1800);
        } catch {
          window.prompt("Copy this link", window.location.href);
        }
      }}
    >
      {done ? "Link copied" : "Copy link"}
    </button>
  );
}

export function CsvButton({ filename, rows, label = "Download CSV" }: { filename: string; rows: (string | number)[][]; label?: string }) {
  return <button className="btn" onClick={() => downloadCsv(filename, rows)}>{label}</button>;
}
