"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

const ITEMS = [
  { href: "/", label: "Findings", code: "FIND", icon: "M4 19V5m0 14h16M8 15l3-4 3 2 4-6" },
  { href: "/compare/", label: "Compare", code: "CMP", icon: "M6 20V10m6 10V4m6 16v-7" },
  { href: "/methodology/", label: "Method", code: "HELP", icon: "M12 17h.01M9.1 9a3 3 0 1 1 3.9 2.9c-.6.3-1 .9-1 1.6V14M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18z" },
];

export default function Nav() {
  const path = usePathname() || "/";
  const active = (href: string) => (href === "/" ? path === "/" || path.startsWith("/company") : path.startsWith(href));
  return (
    <aside className="side" aria-label="Main">
      <Link href="/" className="brand">
        EARNINGS QUALITY<small>Nordic listed companies</small>
      </Link>
      {ITEMS.map((it) => (
        <Link key={it.href} href={it.href} className="navlink" aria-current={active(it.href) ? "page" : undefined}>
          <span style={{ display: "inline-flex", alignItems: "center", gap: 10 }}>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
              <path d={it.icon} />
            </svg>
            {it.label}
          </span>
          <span className="code">{it.code}</span>
        </Link>
      ))}
      <p className="foot">
        Official filings only.<br />
        <a href="https://github.com/MariusFrykhammar/nordic-earnings-quality">Source on GitHub</a>
      </p>
    </aside>
  );
}
