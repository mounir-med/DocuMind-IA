"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { FileStack, MessageSquare } from "lucide-react";
import { toast } from "sonner";
import { Dropzone } from "@/components/documents/Dropzone";
import { Header } from "@/components/layout/Header";
import { Card } from "@/components/ui/Card";
import { EmptyState } from "@/components/ui/EmptyState";
import { Skeleton } from "@/components/ui/Skeleton";
import { StatCard } from "@/components/ui/StatCard";
import { api } from "@/lib/api";
import type { DashboardStats } from "@/lib/types";
import { formatDate } from "@/lib/utils";

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);

  async function load() {
    try {
      setStats(await api.stats());
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "Backend injoignable.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void load();
  }, []);

  async function upload(files: File[]) {
    for (const file of files) {
      try {
        await api.upload(file);
        toast.success(`${file.name} importé.`);
      } catch (error) {
        toast.error(error instanceof Error ? error.message : "Import impossible.");
      }
    }
    await load();
  }

  if (loading) {
    return (
      <div className="grid gap-4 md:grid-cols-4">
        {Array.from({ length: 4 }).map((_, index) => (
          <Skeleton key={index} className="h-28" />
        ))}
      </div>
    );
  }

  if (!stats) {
    return (
      <EmptyState
        icon={FileStack}
        title="Backend injoignable"
        description="Démarrez l’API FastAPI sur le port 8000 puis rechargez."
      />
    );
  }

  return (
    <div className="space-y-6">
      <Header
        subtitle="Assistant documentaire"
        title="Bonjour, prêt à interroger vos PDF."
        actions={
          <Link href="/documents" className="rounded-xl bg-accent px-4 py-2.5 text-sm text-white">
            Importer des PDF
          </Link>
        }
      />

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Documents" value={stats.document_count} />
        <StatCard label="Indexés" value={stats.indexed_count} />
        <StatCard label="Conversations" value={stats.conversation_count} />
        <StatCard label="Questions" value={stats.question_count} />
      </div>

      <Dropzone onFiles={upload} />

      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <h2 className="mb-4 font-semibold">Documents récents</h2>
          {stats.recent_documents.length ? (
            <ul className="space-y-3 text-sm">
              {stats.recent_documents.map((doc) => (
                <li key={doc.id} className="flex justify-between gap-3">
                  <Link href={`/documents/${doc.id}`} className="hover:text-accent">
                    {doc.filename}
                  </Link>
                  <span className="text-muted">{formatDate(doc.created_at)}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-sm text-muted">Aucun document pour le moment.</p>
          )}
        </Card>
        <Card>
          <h2 className="mb-4 font-semibold">Conversations récentes</h2>
          {stats.recent_conversations.length ? (
            <ul className="space-y-3 text-sm">
              {stats.recent_conversations.map((item) => (
                <li key={item.id} className="flex justify-between gap-3">
                  <Link href={`/chat/${item.id}`} className="hover:text-accent">
                    {item.title}
                  </Link>
                  <span className="text-muted">{item.message_count} questions</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-sm text-muted">Aucune conversation.</p>
          )}
        </Card>
      </div>

      <Card>
        <h2 className="mb-4 font-semibold">Activité récente</h2>
        <ul className="space-y-2 text-sm text-muted">
          {stats.recent_documents.slice(0, 3).map((doc) => (
            <li key={`doc-${doc.id}`}>Document importé : {doc.filename}</li>
          ))}
          {stats.recent_conversations.slice(0, 3).map((item) => (
            <li key={`chat-${item.id}`}>Conversation : {item.title}</li>
          ))}
          {!stats.recent_documents.length && !stats.recent_conversations.length ? (
            <li>Aucune activité enregistrée pour le moment.</li>
          ) : null}
        </ul>
      </Card>

      <Card>
        <h2 className="mb-4 font-semibold">Raccourcis</h2>
        <div className="grid gap-3 sm:grid-cols-3">
          <Link href="/chat" className="rounded-xl border border-line p-4 hover:bg-canvas">
            <MessageSquare className="mb-2 h-5 w-5 text-accent" />
            Poser une question
          </Link>
          <Link href="/summaries" className="rounded-xl border border-line p-4 hover:bg-canvas">
            Générer un résumé
          </Link>
          <Link href="/quizzes" className="rounded-xl border border-line p-4 hover:bg-canvas">
            Créer un QCM
          </Link>
        </div>
        <p className="mt-4 text-sm text-muted">
          Fournisseur LLM : {stats.llm_provider}
          {stats.llm_ready ? " (prêt)" : " (mode démo ou non configuré)"} · embeddings{" "}
          {stats.embedding_ready ? "prêts" : "indisponibles"}
        </p>
      </Card>
    </div>
  );
}

