export function ProgressBar({ value, label }: { value: number; label?: string }) {
  const width = Math.min(100, Math.max(0, value));
  return (
    <div>
      {label ? <p className="mb-1 text-sm text-muted">{label}</p> : null}
      <div className="h-2 overflow-hidden rounded-full bg-line">
        <div className="h-full rounded-full bg-accent transition-all" style={{ width: `${width}%` }} />
      </div>
    </div>
  );
}
