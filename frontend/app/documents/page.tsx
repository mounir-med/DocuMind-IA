"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { FileStack, RefreshCw, Trash2 } from "lucide-react";
import { toast } from "sonner";
import { Dropzone } from "@/components/documents/Dropzone";
import { Header } from "@/components/layout/Header";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { ConfirmDialog } from "@/components/ui/Dialog";
import { EmptyState } from "@/components/ui/EmptyState";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { Skeleton } from "@/components/ui/Skeleton";
import { api } from "@/lib/api";
import type { DocumentItem } from "@/lib/types";
import { formatBytes, formatDate, statusLabel } from "@/lib/utils";

export default function DocumentsPage() {
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [query, setQuery] = useState("");
  const [sort, setSort] = useState<"date" | "name" | "status">("date");
  const [status, setStatus] = useState("all");
  const [busy, setBusy] = useState(false);
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState<{ current: number; total: number; name: string } | null>(null);
  const [pendingDelete, setPendingDelete] = useState<DocumentItem | null>(null);

  async function load() {
    try {
      setDocuments(await api.documents());
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "Chargement impossible.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void load();
  }, []);

  async function upload(files: File[]) {
    setBusy(true);
    const pdfs = files.filter((file) => !file.type || file.type === "application/pdf" || file.name.toLowerCase().endsWith(".pdf"));
    for (const [index, file] of pdfs.entries()) {
      setProgress({ current: index, total: pdfs.length, name: file.name });
      try {
        const doc = await api.upload(file);
        toast.success(`${doc.filename} : ${statusLabel(doc.status)}`);
      } catch (error) {
        toast.error(error instanceof Error ? error.message : "Import refusé.");
      }
    }
    setProgress(pdfs.length ? { current: pdfs.length, total: pdfs.length, name: "Terminé" } : null);
    setBusy(false);
    await load();
  }

  const visible = useMemo(() => {
    const filtered = documents.filter(
      (item) =>
        item.filename.toLowerCase().includes(query.toLowerCase()) &&
        (status === "all" || item.status === status),
    );
    return filtered.sort((a, b) => {
      if (sort === "name") return a.filename.localeCompare(b.filename, "fr");
      if (sort === "status") return a.status.localeCompare(b.status);
      return +new Date(b.created_at) - +new Date(a.created_at);
    });
  }, [documents, query, sort, status]);

  return (
    <div className="space-y-6">
      <Header title="Bibliothèque" subtitle="Importez, indexez et consultez vos PDF." />
      <Dropzone onFiles={upload} disabled={busy} />
      {progress ? (
        <ProgressBar
          value={(progress.current / Math.max(progress.total, 1)) * 100}
          label={`Import ${progress.current}/${progress.total} — ${progress.name}`}
        />
      ) : null}
      <div className="flex flex-col gap-3 sm:flex-row">
        <input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Rechercher un document"
          className="w-full rounded-xl border border-line bg-surface px-3 py-2"
        />
        <select
          value={status}
          onChange={(event) => setStatus(event.target.value)}
          className="rounded-xl border border-line bg-surface px-3 py-2"
        >
          <option value="all">Tous les statuts</option>
          <option value="ready">Indexés</option>
          <option value="error">Erreurs</option>
          <option value="scanned">Scannés</option>
          <option value="empty">Texte insuffisant</option>
        </select>
        <select
          value={sort}
          onChange={(event) => setSort(event.target.value as typeof sort)}
          className="rounded-xl border border-line bg-surface px-3 py-2"
        >
          <option value="date">Plus récents</option>
          <option value="name">Nom</option>
          <option value="status">Statut</option>
        </select>
      </div>
      {loading ? (
        <Skeleton className="h-40" />
      ) : visible.length === 0 ? (
        <EmptyState
          icon={FileStack}
          title="Aucun document"
          description="Déposez un PDF pour lancer l’extraction et l’indexation vectorielle."
        />
      ) : (
        <div className="grid gap-4">
          {visible.map((doc) => (
            <Card key={doc.id} className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
              <div>
                <Link href={`/documents/${doc.id}`} className="font-medium hover:text-accent">
                  {doc.filename}
                </Link>
                <p className="mt-1 text-sm text-muted">
                  {formatBytes(doc.size_bytes)} · {doc.page_count} pages · {doc.chunk_count} passages ·{" "}
                  {statusLabel(doc.status)} · {formatDate(doc.created_at)}
                </p>
                {doc.error_message ? <p className="mt-1 text-sm text-red-600">{doc.error_message}</p> : null}
              </div>
              <div className="flex gap-2">
                <Button
                  variant="secondary"
                  onClick={async () => {
                    try {
                      await api.reindex(doc.id);
                      toast.success("Réindexation terminée.");
                      await load();
                    } catch (error) {
                      toast.error(error instanceof Error ? error.message : "Réindexation échouée.");
                    }
                  }}
                >
                  <RefreshCw className="h-4 w-4" /> Réindexer
                </Button>
                <Button variant="danger" onClick={() => setPendingDelete(doc)}>
                  <Trash2 className="h-4 w-4" /> Supprimer
                </Button>
              </div>
            </Card>
          ))}
        </div>
      )}
      <ConfirmDialog
        open={Boolean(pendingDelete)}
        title="Supprimer le document"
        description={pendingDelete ? `${pendingDelete.filename} sera retiré avec son index vectoriel.` : ""}
        confirmLabel="Supprimer"
        danger
        onCancel={() => setPendingDelete(null)}
        onConfirm={async () => {
          if (!pendingDelete) return;
          await api.deleteDocument(pendingDelete.id);
          toast.success("Document supprimé.");
          setPendingDelete(null);
          await load();
        }}
      />
    </div>
  );
}
