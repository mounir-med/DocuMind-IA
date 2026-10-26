"use client";

import { useEffect, useState } from "react";
import { GitCompare } from "lucide-react";
import { toast } from "sonner";
import { DocumentPicker } from "@/components/documents/DocumentPicker";
import { MarkdownMessage } from "@/components/chat/MarkdownMessage";
import { SourceList } from "@/components/sources/SourceList";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { EmptyState } from "@/components/ui/EmptyState";
import { api } from "@/lib/api";
import type { DocumentItem, SourceItem } from "@/lib/types";

export default function ComparePage() {
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [selected, setSelected] = useState<string[]>([]);
  const [question, setQuestion] = useState("Compare les thèmes, différences et éventuelles contradictions.");
  const [content, setContent] = useState("");
  const [sources, setSources] = useState<SourceItem[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.documents().then(setDocuments).catch((error) => toast.error(error.message));
  }, []);

  async function run() {
    if (selected.length < 2) return toast.error("Sélectionnez au moins deux documents.");
    setLoading(true);
    try {
      const result = await api.compare(selected, question);
      setContent(result.content);
      setSources(result.sources);
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "Comparaison impossible.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-3xl font-semibold">Comparaison</h1>
        <p className="text-muted">Une divergence n’est pas déclarée contradiction certaine sans opposition claire.</p>
      </header>
      <Card className="space-y-4">
        <DocumentPicker documents={documents} selected={selected} onChange={setSelected} />
        <textarea
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          className="min-h-24 w-full rounded-xl border border-line bg-canvas px-3 py-2"
        />
        <Button onClick={() => void run()} disabled={loading}>
          {loading ? "Analyse…" : "Comparer"}
        </Button>
      </Card>
      {content ? (
        <Card className="space-y-4">
          <MarkdownMessage content={content} />
          <SourceList sources={sources} />
        </Card>
      ) : (
        <EmptyState
          icon={GitCompare}
          title="Aucune comparaison"
          description="Choisissez deux PDF ou plus, puis lancez l’analyse comparative."
        />
      )}
    </div>
  );
}
