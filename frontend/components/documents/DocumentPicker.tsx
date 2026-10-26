"use client";

import type { DocumentItem } from "@/lib/types";

export function DocumentPicker({
  documents,
  selected,
  onChange,
  multiple = true,
}: {
  documents: DocumentItem[];
  selected: string[];
  onChange: (ids: string[]) => void;
  multiple?: boolean;
}) {
  const ready = documents.filter((item) => item.status === "ready");

  function toggle(id: string) {
    if (!multiple) {
      onChange([id]);
      return;
    }
    onChange(selected.includes(id) ? selected.filter((item) => item !== id) : [...selected, id]);
  }

  if (!ready.length) {
    return <p className="text-sm text-muted">Aucun document indexé. Importez un PDF d’abord.</p>;
  }

  return (
    <div className="flex flex-wrap gap-2">
      {ready.map((doc) => {
        const active = selected.includes(doc.id);
        return (
          <button
            key={doc.id}
            type="button"
            onClick={() => toggle(doc.id)}
            className={`rounded-full border px-3 py-1.5 text-sm ${
              active ? "border-accent bg-accent/10 text-accent" : "border-line"
            }`}
          >
            {doc.filename}
          </button>
        );
      })}
    </div>
  );
}
