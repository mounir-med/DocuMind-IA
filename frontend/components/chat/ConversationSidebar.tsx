"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { Plus } from "lucide-react";
import { toast } from "sonner";
import { Button } from "@/components/ui/Button";
import { api } from "@/lib/api";
import type { ConversationItem } from "@/lib/types";
import { cn, formatDate } from "@/lib/utils";

export function ConversationSidebar() {
  const pathname = usePathname();
  const router = useRouter();
  const [items, setItems] = useState<ConversationItem[]>([]);

  async function load() {
    try {
      setItems(await api.conversations());
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "Conversations indisponibles.");
    }
  }

  useEffect(() => {
    void load();
  }, [pathname]);

  return (
    <aside className="hidden h-[calc(100vh-6rem)] flex-col rounded-2xl border border-line bg-surface p-3 xl:flex">
      <Button
        className="mb-3 w-full"
        onClick={async () => {
          const conversation = await api.createConversation();
          router.push(`/chat/${conversation.id}`);
        }}
      >
        <Plus className="h-4 w-4" /> Nouvelle
      </Button>
      <div className="min-h-0 flex-1 space-y-1 overflow-y-auto">
        {items.map((item) => {
          const active = pathname === `/chat/${item.id}`;
          return (
            <Link
              key={item.id}
              href={`/chat/${item.id}`}
              className={cn(
                "block rounded-xl px-3 py-2 text-sm hover:bg-canvas",
                active && "bg-accent/10 text-accent",
              )}
            >
              <p className="truncate font-medium">{item.title}</p>
              <p className="text-xs text-muted">{formatDate(item.updated_at)}</p>
            </Link>
          );
        })}
      </div>
    </aside>
  );
}
