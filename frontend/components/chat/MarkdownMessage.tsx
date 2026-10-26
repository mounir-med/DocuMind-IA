"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export function MarkdownMessage({ content }: { content: string }) {
  return (
    <div className="prose prose-sm dark:prose-invert max-w-none text-[15px] leading-7">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          code({ className, children }) {
            return (
              <code className={`rounded bg-canvas px-1.5 py-0.5 ${className ?? ""}`}>{children}</code>
            );
          },
          pre({ children }) {
            return <pre className="overflow-x-auto rounded-xl bg-canvas p-3">{children}</pre>;
          },
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
