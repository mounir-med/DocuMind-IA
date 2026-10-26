"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import {
  BookOpen,
  FileStack,
  GitCompare,
  LayoutDashboard,
  Menu,
  MessageSquare,
  Moon,
  Settings,
  Sparkles,
  Sun,
  X,
} from "lucide-react";
import { cn } from "@/lib/utils";

const NAV = [
  { href: "/", label: "Tableau de bord", icon: LayoutDashboard },
  { href: "/documents", label: "Documents", icon: FileStack },
  { href: "/chat", label: "Chat IA", icon: MessageSquare },
  { href: "/summaries", label: "Résumés", icon: BookOpen },
  { href: "/quizzes", label: "QCM", icon: Sparkles },
  { href: "/compare", label: "Comparaison", icon: GitCompare },
  { href: "/settings", label: "Paramètres", icon: Settings },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const [dark, setDark] = useState(false);

  useEffect(() => {
    const stored = localStorage.getItem("documind-theme");
    const enabled = stored ? stored === "dark" : window.matchMedia("(prefers-color-scheme: dark)").matches;
    setDark(enabled);
    document.documentElement.classList.toggle("dark", enabled);
  }, []);

  function toggleTheme() {
    const next = !dark;
    setDark(next);
    document.documentElement.classList.toggle("dark", next);
    localStorage.setItem("documind-theme", next ? "dark" : "light");
  }

  return (
    <div className="min-h-screen bg-canvas text-ink">
      <div className="lg:hidden sticky top-0 z-30 flex items-center justify-between border-b border-line bg-surface/90 px-4 py-3 backdrop-blur">
        <button type="button" onClick={() => setOpen(true)} className="rounded-lg p-2 hover:bg-canvas" aria-label="Menu">
          <Menu className="h-5 w-5" />
        </button>
        <span className="font-semibold">DocuMind AI</span>
        <button type="button" onClick={toggleTheme} className="rounded-lg p-2 hover:bg-canvas" aria-label="Thème">
          {dark ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
        </button>
      </div>

      {open ? (
        <div className="fixed inset-0 z-40 bg-black/40 lg:hidden" onClick={() => setOpen(false)}>
          <aside className="h-full w-72 bg-surface p-4" onClick={(event) => event.stopPropagation()}>
            <div className="mb-6 flex items-center justify-between">
              <Brand />
              <button type="button" onClick={() => setOpen(false)} aria-label="Fermer">
                <X className="h-5 w-5" />
              </button>
            </div>
            <NavList pathname={pathname} onNavigate={() => setOpen(false)} />
          </aside>
        </div>
      ) : null}

      <div className="mx-auto flex min-h-screen max-w-[1600px]">
        <aside className="hidden w-72 shrink-0 border-r border-line bg-surface/80 p-5 lg:block">
          <div className="mb-8 flex items-center justify-between">
            <Brand />
            <button type="button" onClick={toggleTheme} className="rounded-lg p-2 hover:bg-canvas" aria-label="Thème">
              {dark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
            </button>
          </div>
          <NavList pathname={pathname} />
        </aside>
        <main className="min-w-0 flex-1 p-4 sm:p-6 lg:p-8">{children}</main>
      </div>
    </div>
  );
}

function Brand() {
  return (
    <Link href="/" className="flex items-center gap-2 font-semibold">
      <span className="grid h-9 w-9 place-items-center rounded-xl bg-accent text-white">DM</span>
      DocuMind AI
    </Link>
  );
}

function NavList({ pathname, onNavigate }: { pathname: string; onNavigate?: () => void }) {
  return (
    <nav className="space-y-1">
      {NAV.map((item) => {
        const active = item.href === "/" ? pathname === "/" : pathname.startsWith(item.href);
        const Icon = item.icon;
        return (
          <Link
            key={item.href}
            href={item.href}
            onClick={onNavigate}
            className={cn(
              "flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm transition",
              active ? "bg-accent/10 text-accent" : "text-muted hover:bg-canvas hover:text-ink",
            )}
          >
            <Icon className="h-4 w-4" />
            {item.label}
          </Link>
        );
      })}
    </nav>
  );
}
