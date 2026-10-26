"use client";

import { Upload } from "lucide-react";
import { useState } from "react";

export function Dropzone({
  onFiles,
  disabled,
}: {
  onFiles: (files: File[]) => void;
  disabled?: boolean;
}) {
  const [over, setOver] = useState(false);

  function take(list: FileList | null) {
    if (!list) return;
    onFiles(Array.from(list).filter((file) => file.name.toLowerCase().endsWith(".pdf")));
  }

  return (
    <label
      className={`grid cursor-pointer place-items-center rounded-2xl border border-dashed px-6 py-10 text-center transition ${
        over ? "border-accent bg-accent/5" : "border-line bg-surface"
      } ${disabled ? "pointer-events-none opacity-60" : ""}`}
      onDragOver={(event) => {
        event.preventDefault();
        setOver(true);
      }}
      onDragLeave={() => setOver(false)}
      onDrop={(event) => {
        event.preventDefault();
        setOver(false);
        take(event.dataTransfer.files);
      }}
    >
      <Upload className="mb-3 h-8 w-8 text-accent" />
      <p className="font-medium">Glissez-déposez vos PDF</p>
      <p className="mt-1 text-sm text-muted">ou cliquez pour parcourir. Validation aussi côté serveur.</p>
      <input
        type="file"
        accept="application/pdf,.pdf"
        multiple
        className="hidden"
        disabled={disabled}
        onChange={(event) => take(event.target.files)}
      />
    </label>
  );
}
