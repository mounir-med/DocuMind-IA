import type { ReactNode } from "react";
import { Suspense } from "react";

export default function DocumentLayout({ children }: { children: ReactNode }) {
  return <Suspense fallback={<p className="text-muted">Chargement du visualiseur…</p>}>{children}</Suspense>;
}
