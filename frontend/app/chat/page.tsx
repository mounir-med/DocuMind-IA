"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { MessageSquare, Plus, Trash2 } from "lucide-react";
import { toast } from "sonner";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { EmptyState } from "@/components/ui/EmptyState";
import { api } from "@/lib/api";
import type { ConversationItem } from "@/lib/types";
import { formatDate } from "@/lib/utils";

export default function ChatListPage() {
  const router = useRouter();
  const [items, setItems] = useState<ConversationItem[]>([]);

  async function load() {
    try {
      setItems(await api.conversations());
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "Impossible de charger les conversations.");
    }
  }

  useEffect(() => {
    void load();
  }, []);

  async function create() {
    const conversation = await api.createConversation();
    router.push(`/chat/${conversation.id}`);
  }

  return (
    <div className="space-y-6">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-semibold">Chat IA</h1>
          <p className="text-muted">Interrogez vos documents avec un pipeline RAG.</p>
        </div>
        <Button onClick={() => void create()}>
          <Plus className="h-4 w-4" /> Nouvelle conversation
        </Button>
      </header>
      {items.length === 0 ? (
        <EmptyState
          icon={MessageSquare}
          title="Aucune conversation"
          description="Créez une conversation, sélectionnez des PDF, puis posez une question en français."
          action={<Button onClick={() => void create()}>Commencer</Button>}
        />
      ) : (
        <div className="grid gap-3">
          {items.map((item) => (
            <Card key={item.id} className="flex items-center justify-between gap-3">
              <button type="button" className="text-left" onClick={() => router.push(`/chat/${item.id}`)}>
                <p className="font-medium">{item.title}</p>
                <p className="text-sm text-muted">
                  {item.message_count} questions · {formatDate(item.updated_at)}
                </p>
              </button>
              <Button
                variant="ghost"
                onClick={async () => {
                  if (!confirm("Supprimer cette conversation ?")) return;
                  await api.deleteConversation(item.id);
                  await load();
                }}
              >
                <Trash2 className="h-4 w-4" />
              </Button>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
