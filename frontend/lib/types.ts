export type DocumentStatus = "empty" | "indexing" | "ready" | "scanned" | "error";

export interface DocumentItem {
  id: string;
  filename: string;
  sha256: string;
  size_bytes: number;
  page_count: number;
  chunk_count: number;
  status: DocumentStatus | string;
  error_message?: string | null;
  created_at: string;
  indexed_at?: string | null;
}

export interface SourceItem {
  chunk_id: string;
  document_id: string;
  document_name: string;
  page_number: number;
  excerpt: string;
  score: number | null;
}

export interface GenerationMeta {
  provider?: string;
  model?: string;
  demo?: boolean;
  error?: string | null;
  usage?: Record<string, unknown>;
  insufficient_context?: boolean;
  [key: string]: unknown;
}

export interface ChatMessage {
  id: string;
  conversation_id: string;
  role: "user" | "assistant" | string;
  content: string;
  sources: SourceItem[];
  generation: GenerationMeta;
  created_at: string;
}

export interface ConversationItem {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
  message_count: number;
  messages?: ChatMessage[];
}

export interface SendMessageResult {
  user_message: ChatMessage;
  assistant_message: ChatMessage;
}

export interface QuizChoice {
  id: string;
  text: string;
}

export interface QuizQuestion {
  id: string;
  question: string;
  choices: QuizChoice[];
  correct_choice_id: string;
  explanation: string;
  source?: SourceItem | null;
}

export interface QuizResult {
  document_ids: string[];
  level: string;
  questions: QuizQuestion[];
  notice?: string | null;
  generation: GenerationMeta;
}

export interface GeneratedText {
  content: string;
  sources: SourceItem[];
  generation: GenerationMeta;
}

export interface SummaryResult extends GeneratedText {
  document_id: string;
  kind: string;
}

export interface DashboardStats {
  document_count: number;
  indexed_count: number;
  conversation_count: number;
  question_count: number;
  recent_documents: DocumentItem[];
  recent_conversations: ConversationItem[];
  llm_provider: string;
  llm_ready: boolean;
  embedding_ready: boolean;
}

export interface PublicSettings {
  llm_provider: string;
  llm_model: string;
  llm_temperature: number;
  llm_configured: boolean;
  has_api_key: boolean;
  embedding_provider: string;
  embedding_model: string;
  rag_top_k: number;
  rag_score_threshold: number;
  chunk_size: number;
  chunk_overlap: number;
  max_upload_mb: number;
  app_name: string;
  app_version: string;
}

export type SettingsUpdate = Partial<
  Pick<
    PublicSettings,
    "llm_provider" | "llm_model" | "llm_temperature" | "rag_top_k" | "rag_score_threshold"
  >
>;
