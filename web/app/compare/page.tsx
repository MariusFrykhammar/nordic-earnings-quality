import type { Metadata } from "next";
import Compare from "@/components/Compare";

export const metadata: Metadata = { title: "Compare companies: earnings quality" };

export default function ComparePage() {
  return (
    <section style={{ marginTop: 0 }}>
      <h1>Compare companies</h1>
      <p className="lede">Pick up to six companies to set growth, margins and cash conversion side by side.</p>
      <Compare />
    </section>
  );
}
