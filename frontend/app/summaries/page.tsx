"use client";

import { useEffect, useRef, useState } from "react";
import { BookOpen } from "lucide-react";
import { toast } from "sonner";
import { DocumentPicker } from "@/components/documents/DocumentPicker";
import { MarkdownMessage } from "@/components/chat/MarkdownMessage";
import { SourceList } from "@/components/sources/SourceList";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { EmptyState } from "@/components/ui/EmptyState";
import { api } from "@/lib/api";
import type { DocumentItem, SourceItem } from "@/lib/types";

const KINDS = [
  { id: "short", label: "Résumé court" },
  { id: "detailed", label: "Résumé détaillé" },
  { id: "chapters", label: "Chapitre par chapitre" },
  { id: "ideas", label: "Idées principales" },
  { id: "definitions", label: "Définitions" },
  { id: "revision", label: "Fiche de révision" },
];

export default function SummariesPage() {
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [selected, setSelected] = useState<string[]>([]);
  const [kind, setKind] = useState("short");
  const [content, setContent] = useState("");
  const [sources, setSources] = useState<SourceItem[]>([]);
  const [loading, setLoading] = useState(false);
  const requestVersion = useRef(0);

  useEffect(() => {
    api.documents().then(setDocuments).catch((error) => toast.error(error.message));
  }, []);

  async function run() {
    if (!selected[0]) return toast.error("Sélectionnez un document.");
    setContent("");
    setSources([]);
    const version = ++requestVersion.current;
    const requestedDocument = selected[0];
    const requestedKind = kind;
    setLoading(true);
    try {
      const result = await api.summarize(requestedDocument, requestedKind);
      if (version !== requestVersion.current) return;
      setContent(result.content);
      setSources(result.sources);
    } catch (error) {
      if (version !== requestVersion.current) return;
      toast.error(error instanceof Error ? error.message : "Résumé impossible.");
    } finally {
      if (version === requestVersion.current) setLoading(false);
    }
  }

  function changeSelection(ids: string[]) {
    requestVersion.current += 1;
    setLoading(false);
    setSelected(ids);
    setContent("");
    setSources([]);
  }

  function changeKind(nextKind: string) {
    requestVersion.current += 1;
    setLoading(false);
    setKind(nextKind);
    setContent("");
    setSources([]);
  }

  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-3xl font-semibold">Résumés</h1>
        <p className="text-muted">Les synthèses s’appuient sur les passages indexés du document choisi.</p>
      </header>
      <Card className="space-y-4">
        <DocumentPicker documents={documents} selected={selected} onChange={changeSelection} multiple={false} />
        <div className="flex flex-wrap gap-2">
          {KINDS.map((item) => (
            <button
              key={item.id}
              type="button"
              onClick={() => changeKind(item.id)}
              className={`rounded-full border px-3 py-1.5 text-sm ${
                kind === item.id ? "border-accent bg-accent/10 text-accent" : "border-line"
              }`}
            >
              {item.label}
            </button>
          ))}
        </div>
        <Button onClick={() => void run()} disabled={loading}>
          {loading ? "Génération…" : "Générer"}
        </Button>
      </Card>
      {content ? (
        <Card className="space-y-4">
          <MarkdownMessage content={content} />
          <SourceList sources={sources} />
        </Card>
      ) : (
        <EmptyState icon={BookOpen} title="Aucun résumé" description="Choisissez un PDF indexé puis un type de synthèse." />
      )}
    </div>
  );
}
