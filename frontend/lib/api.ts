import type {
  ConversationItem,
  DashboardStats,
  DocumentItem,
  GeneratedText,
  PublicSettings,
  QuizResult,
  SendMessageResult,
  SettingsUpdate,
  SummaryResult,
} from "./types";

export const API_URL = (process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000").replace(/\/$/, "");

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${API_URL}${path}`, init);
  } catch {
    throw new Error("Backend injoignable. Vérifiez qu'il tourne sur " + API_URL);
  }
  if (!response.ok) {
    let message = `Erreur ${response.status}`;
    try {
      const data = await response.json();
      if (typeof data.detail === "string") message = data.detail;
      else if (Array.isArray(data.detail)) message = data.detail.map((d: { msg?: string }) => d.msg).join(" ; ");
    } catch {
      /* corps non JSON */
    }
    throw new Error(message);
  }
  return (await response.json()) as T;
}

function json(method: string, body?: unknown): RequestInit {
  return {
    method,
    headers: { "Content-Type": "application/json" },
    body: body === undefined ? undefined : JSON.stringify(body),
  };
}

export const api = {
  // Documents
  documents: () => request<DocumentItem[]>("/api/documents"),
  document: (id: string) => request<DocumentItem>(`/api/documents/${id}`),
  upload: (file: File) => {
    const form = new FormData();
    form.append("file", file);
    return request<DocumentItem>("/api/documents/upload", { method: "POST", body: form });
  },
  deleteDocument: (id: string) => request<{ ok: boolean }>(`/api/documents/${id}`, { method: "DELETE" }),
  reindex: (id: string) => request<DocumentItem>(`/api/documents/${id}/index`, { method: "POST" }),
  pageText: (id: string, page: number) =>
    request<{ document_id: string; page_number: number; text: string }>(`/api/documents/${id}/pages/${page}`),
  fileUrl: (id: string) => `${API_URL}/api/documents/${id}/file`,

  // Génération
  summarize: (id: string, kind: string) =>
    request<SummaryResult>(`/api/documents/${id}/summarize`, json("POST", { kind })),
  quiz: (id: string, count: number, level: string, documentIds: string[]) =>
    request<QuizResult>(`/api/documents/${id}/quiz`, json("POST", { count, level, document_ids: documentIds })),
  compare: (documentIds: string[], question: string) =>
    request<GeneratedText>("/api/documents/compare", json("POST", { document_ids: documentIds, question })),

  // Conversations
  conversations: () => request<ConversationItem[]>("/api/conversations"),
  conversation: (id: string) => request<ConversationItem>(`/api/conversations/${id}`),
  createConversation: (title = "Nouvelle conversation") =>
    request<ConversationItem>("/api/conversations", json("POST", { title })),
  deleteConversation: (id: string) => request<{ ok: boolean }>(`/api/conversations/${id}`, { method: "DELETE" }),
  clearConversations: () => request<{ deleted: number }>("/api/conversations", { method: "DELETE" }),
  sendMessage: (conversationId: string, content: string, documentIds: string[], regenerate = false) =>
    request<SendMessageResult>(
      `/api/chat/${conversationId}/messages`,
      json("POST", { content, document_ids: documentIds, regenerate }),
    ),

  // Tableau de bord & paramètres
  stats: () => request<DashboardStats>("/api/dashboard/stats"),
  settings: () => request<PublicSettings>("/api/settings"),
  updateSettings: (payload: SettingsUpdate) => request<PublicSettings>("/api/settings", json("PUT", payload)),
  diagnoseLLM: () => request<{ ok: boolean; provider: string; model?: string; code?: string; message: string }>("/api/settings/diagnose", json("POST")),
};
