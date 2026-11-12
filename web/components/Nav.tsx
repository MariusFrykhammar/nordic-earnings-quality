"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

const ITEMS = [
  { href: "/", label: "Findings" },
  { href: "/compare/", label: "Compare" },
  { href: "/methodology/", label: "Methodology" },
  { href: "/about/", label: "About" },
];

/** Logo mark: two lines that start together and part ways (profit and cash). */
function Mark() {
  return (
    <svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M3 17 L10 13 L21 4" fill="none" stroke="var(--profit)" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M3 17 L10 13 L21 19" fill="none" stroke="var(--cash)" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

export default function Nav() {
  const path = usePathname() || "/";
  const active = (href: string) => (href === "/" ? path === "/" || path.startsWith("/company") : path.startsWith(href));
  return (
    <header className="top">
      <div className="top-inner">
        <Link href="/" className="brand">
          <Mark />
          <span>Earnings Quality<span className="brand-sub">Nordic</span></span>
        </Link>
        <nav aria-label="Main" className="topnav">
          {ITEMS.map((it) => (
            <Link key={it.href} href={it.href} aria-current={active(it.href) ? "page" : undefined}>
              {it.label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}
