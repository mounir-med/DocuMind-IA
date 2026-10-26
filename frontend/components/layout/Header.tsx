import type { ReactNode } from "react";

export function Header({
  title,
  subtitle,
  actions,
}: {
  title: string;
  subtitle?: string;
  actions?: ReactNode;
}) {
  return (
    <header className="flex flex-wrap items-end justify-between gap-4">
      <div>
        {subtitle ? <p className="text-sm text-muted">{subtitle}</p> : null}
        <h1 className="text-3xl font-semibold tracking-tight">{title}</h1>
      </div>
      {actions}
    </header>
  );
}
