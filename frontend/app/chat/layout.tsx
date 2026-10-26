import type { ReactNode } from "react";
import { ConversationSidebar } from "@/components/chat/ConversationSidebar";

export default function ChatLayout({ children }: { children: ReactNode }) {
  return (
    <div className="grid gap-4 xl:grid-cols-[260px_minmax(0,1fr)]">
      <ConversationSidebar />
      <div className="min-w-0">{children}</div>
    </div>
  );
}
