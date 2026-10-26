"use client";

import { useParams, useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import { Copy, RefreshCw, Send, Trash2 } from "lucide-react";
import { toast } from "sonner";
import { MarkdownMessage } from "@/components/chat/MarkdownMessage";
import { DocumentPicker } from "@/components/documents/DocumentPicker";
import { SourceList } from "@/components/sources/SourceList";
import { Button } from "@/components/ui/Button";
import { ConfirmDialog } from "@/components/ui/Dialog";
import { api } from "@/lib/api";
import type { ChatMessage, ConversationItem, DocumentItem } from "@/lib/types";

export default function ChatThreadPage() {
  const params = useParams<{ id: string }>();
  const router = useRouter();
  const [conversation, setConversation] = useState<ConversationItem | null>(null);
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [selected, setSelected] = useState<string[]>([]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(false);
  const bottom = useRef<HTMLDivElement>(null);

  async function load() {
    const [thread, docs] = await Promise.all([api.conversation(params.id), api.documents()]);
    setConversation(thread);
    setDocuments(docs);
    if (!selected.length) {
      setSelected(docs.filter((item) => item.status === "ready").map((item) => item.id));
    }
  }

  useEffect(() => {
    void load().catch((error) => toast.error(error instanceof Error ? error.message : "Chargement impossible."));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [params.id]);

  useEffect(() => {
    bottom.current?.scrollIntoView({ behavior: "smooth" });
  }, [conversation?.messages, sending]);

  async function send(regenerate = false) {
    if (!regenerate && !input.trim()) return;
    setSending(true);
    try {
      const result = await api.sendMessage(params.id, input.trim() || " ", selected, regenerate);
      setInput("");
      setConversation((current) => {
        if (!current) return current;
        const messages = [...(current.messages ?? []).filter((item) => item.id !== result.assistant_message.id)];
        if (!regenerate) messages.push(result.user_message);
        else {
          const withoutLastAssistant = [...(current.messages ?? [])];
          const lastAssistant = [...withoutLastAssistant].reverse().find((item) => item.role === "assistant");
          const next = lastAssistant
            ? withoutLastAssistant.filter((item) => item.id !== lastAssistant.id)
            : withoutLastAssistant;
          next.push(result.assistant_message);
          return { ...current, messages: next };
        }
        messages.push(result.assistant_message);
        return { ...current, messages };
      });
      await load();
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "Génération impossible.");
    } finally {
      setSending(false);
    }
  }

  const messages: ChatMessage[] = conversation?.messages ?? [];

  return (
    <div className="grid h-[calc(100vh-6rem)] grid-rows-[auto_minmax(0,1fr)_auto] gap-4">
      <header className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl font-semibold">{conversation?.title ?? "Conversation"}</h1>
          <p className="text-sm text-muted">Les sources affichées viennent uniquement du retriever.</p>
        </div>
        <Button variant="danger" onClick={() => setConfirmDelete(true)}>
          <Trash2 className="h-4 w-4" /> Supprimer
        </Button>
      </header>

      <div className="overflow-y-auto rounded-2xl border border-line bg-surface p-4">
        <div className="mb-4">
          <p className="mb-2 text-sm font-medium">Documents ciblés</p>
          <DocumentPicker documents={documents} selected={selected} onChange={setSelected} />
          <label className="mt-2 flex items-center gap-2 text-sm text-muted">
            <input
              type="checkbox"
              checked={selected.length === documents.filter((item) => item.status === "ready").length}
              onChange={(event) =>
                setSelected(
                  event.target.checked ? documents.filter((item) => item.status === "ready").map((item) => item.id) : [],
                )
              }
            />
            Rechercher dans tous les documents indexés
          </label>
        </div>
        <div className="space-y-4">
          {messages.map((message) => (
            <article
              key={message.id}
              className={`max-w-3xl rounded-2xl px-4 py-3 ${
                message.role === "user" ? "ml-auto bg-accent text-white" : "bg-canvas"
              }`}
            >
              {message.role === "assistant" ? (
                <>
                  <MarkdownMessage content={message.content} />
                  {Boolean(message.generation?.demo) ? (
                    <p className="mt-2 text-xs text-muted">Mode démonstration : pas de génération LLM réelle.</p>
                  ) : null}
                  <div className="mt-3 flex gap-2">
                    <Button
                      variant="secondary"
                      onClick={async () => {
                        await navigator.clipboard.writeText(message.content);
                        toast.success("Réponse copiée.");
                      }}
                    >
                      <Copy className="h-4 w-4" /> Copier
                    </Button>
                    <Button variant="secondary" onClick={() => void send(true)}>
                      <RefreshCw className="h-4 w-4" /> Régénérer
                    </Button>
                  </div>
                  <div className="mt-4">
                    <SourceList sources={message.sources} />
                  </div>
                </>
              ) : (
                <p>{message.content}</p>
              )}
            </article>
          ))}
          {sending ? <p className="text-sm text-muted">Recherche des passages et génération…</p> : null}
          <div ref={bottom} />
        </div>
      </div>

      <form
        className="flex gap-2"
        onSubmit={(event) => {
          event.preventDefault();
          void send(false);
        }}
      >
        <textarea
          value={input}
          onChange={(event) => setInput(event.target.value)}
          placeholder="Posez une question, par exemple : Résume ce document en dix points."
          className="min-h-14 flex-1 rounded-2xl border border-line bg-surface px-4 py-3"
          onKeyDown={(event) => {
            if (event.key === "Enter" && !event.shiftKey) {
              event.preventDefault();
              void send(false);
            }
          }}
        />
        <Button type="submit" disabled={sending}>
          <Send className="h-4 w-4" />
        </Button>
      </form>
      <ConfirmDialog
        open={confirmDelete}
        title="Supprimer la conversation"
        description="L’historique de cette discussion sera perdu."
        confirmLabel="Supprimer"
        danger
        onCancel={() => setConfirmDelete(false)}
        onConfirm={async () => {
          await api.deleteConversation(params.id);
          router.push("/chat");
        }}
      />
    </div>
  );
}
