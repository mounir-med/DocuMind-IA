import Link from "next/link";
import type { SourceItem } from "@/lib/types";

export function SourceList({ sources }: { sources: SourceItem[] }) {
  if (!sources.length) {
    return <p className="text-sm text-muted">Aucune source retrouvée pour cette réponse.</p>;
  }
  return (
    <div className="space-y-3">
      {sources.map((source) => (
        <article key={source.chunk_id} className="rounded-xl border border-line bg-canvas p-3">
          <div className="flex flex-wrap items-center justify-between gap-2 text-sm">
            <strong>{source.document_name}</strong>
            <span className="text-muted">
              page {source.page_number}
              {source.score !== null ? ` · score ${source.score.toFixed(2)}` : ""}
            </span>
          </div>
          <p className="mt-2 text-sm text-muted">{source.excerpt}</p>
          <Link
            href={`/documents/${source.document_id}?page=${source.page_number}`}
            className="mt-2 inline-block text-sm text-accent hover:underline"
          >
            Ouvrir le document
          </Link>
        </article>
      ))}
    </div>
  );
}
