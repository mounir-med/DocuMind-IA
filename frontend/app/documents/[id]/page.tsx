"use client";

import { useParams, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import { toast } from "sonner";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { api } from "@/lib/api";
import type { DocumentItem } from "@/lib/types";
import { formatBytes, formatDate, statusLabel } from "@/lib/utils";

export default function DocumentViewerPage() {
  const params = useParams<{ id: string }>();
  const search = useSearchParams();
  const [doc, setDoc] = useState<DocumentItem | null>(null);
  const [page, setPage] = useState(Number(search.get("page") || "1"));
  const [text, setText] = useState("");
  const [zoom, setZoom] = useState(100);

  useEffect(() => {
    async function load() {
      try {
        const item = await api.document(params.id);
        setDoc(item);
        const initial = Number(search.get("page") || "1");
        setPage(Math.min(Math.max(initial, 1), item.page_count || 1));
      } catch (error) {
        toast.error(error instanceof Error ? error.message : "Document introuvable.");
      }
    }
    void load();
  }, [params.id, search]);

  useEffect(() => {
    if (!doc) return;
    api
      .pageText(doc.id, page)
      .then((result) => setText(result.text))
      .catch(() => setText(""));
  }, [doc, page]);

  if (!doc) return <p className="text-muted">Chargement du document…</p>;

  return (
    <div className="grid gap-4 xl:grid-cols-[minmax(0,1fr)_320px]">
      <Card className="space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <h1 className="text-xl font-semibold">{doc.filename}</h1>
          <div className="flex gap-2">
            <Button variant="secondary" onClick={() => setZoom((value) => Math.max(70, value - 10))}>
              Zoom -
            </Button>
            <Button variant="secondary" onClick={() => setZoom((value) => Math.min(160, value + 10))}>
              Zoom +
            </Button>
          </div>
        </div>
        <iframe
          title={doc.filename}
          src={`${api.fileUrl(doc.id)}#page=${page}`}
          className="h-[70vh] w-full rounded-xl border border-line bg-white"
          style={{ transform: `scale(${zoom / 100})`, transformOrigin: "top left", width: `${10000 / zoom}%` }}
        />
        <div className="flex items-center justify-between">
          <Button variant="secondary" disabled={page <= 1} onClick={() => setPage((value) => value - 1)}>
            Page précédente
          </Button>
          <span className="text-sm text-muted">
            Page {page} / {doc.page_count || 1}
          </span>
          <Button
            variant="secondary"
            disabled={page >= (doc.page_count || 1)}
            onClick={() => setPage((value) => value + 1)}
          >
            Page suivante
          </Button>
        </div>
      </Card>
      <div className="space-y-4">
        <Card>
          <h2 className="font-semibold">Informations</h2>
          <ul className="mt-3 space-y-2 text-sm text-muted">
            <li>Statut : {statusLabel(doc.status)}</li>
            <li>Taille : {formatBytes(doc.size_bytes)}</li>
            <li>Pages : {doc.page_count}</li>
            <li>Passages : {doc.chunk_count}</li>
            <li>Import : {formatDate(doc.created_at)}</li>
            <li>Empreinte : {doc.sha256.slice(0, 12)}…</li>
          </ul>
          {doc.error_message ? <p className="mt-3 text-sm text-red-600">{doc.error_message}</p> : null}
        </Card>
        <Card>
          <h2 className="font-semibold">Texte de la page {page}</h2>
          <p className="mt-3 whitespace-pre-wrap text-sm text-muted">
            {text || "Aucun texte extractible sur cette page."}
          </p>
        </Card>
      </div>
    </div>
  );
}
