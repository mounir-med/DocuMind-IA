"use client";

import { useEffect, useState } from "react";
import { toast } from "sonner";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { api } from "@/lib/api";
import type { PublicSettings } from "@/lib/types";

export default function SettingsPage() {
  const [settings, setSettings] = useState<PublicSettings | null>(null);
  const [diagnosis, setDiagnosis] = useState<{ ok: boolean; message: string } | null>(null);
  const [diagnosing, setDiagnosing] = useState(false);

  useEffect(() => {
    api.settings().then(setSettings).catch((error) => toast.error(error.message));
  }, []);

  async function save() {
    if (!settings) return;
    try {
      const updated = await api.updateSettings({
        llm_provider: settings.llm_provider,
        llm_model: settings.llm_model,
        llm_temperature: settings.llm_temperature,
        rag_top_k: settings.rag_top_k,
        rag_score_threshold: settings.rag_score_threshold,
      });
      setSettings(updated);
      toast.success("Paramètres enregistrés.");
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "Enregistrement impossible.");
    }
  }

  if (!settings) return <p className="text-muted">Chargement des paramètres…</p>;

  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-3xl font-semibold">Paramètres</h1>
        <p className="text-muted">Les clés API restent côté serveur et ne sont jamais renvoyées.</p>
      </header>
      <Card className="space-y-4">
        <label className="block text-sm">
          Fournisseur LLM
          <select
            value={settings.llm_provider}
            onChange={(event) => setSettings({ ...settings, llm_provider: event.target.value })}
            className="mt-1 w-full rounded-xl border border-line bg-canvas px-3 py-2"
          >
            <option value="demo">Démo (sans génération réelle)</option>
            <option value="openai">OpenAI compatible</option>
            <option value="ollama">Ollama local</option>
          </select>
        </label>
        <label className="block text-sm">
          Modèle
          <input
            value={settings.llm_model}
            onChange={(event) => setSettings({ ...settings, llm_model: event.target.value })}
            className="mt-1 w-full rounded-xl border border-line bg-canvas px-3 py-2"
          />
        </label>
        <label className="block text-sm">
          Température ({settings.llm_temperature})
          <input
            type="range"
            min={0}
            max={1}
            step={0.05}
            value={settings.llm_temperature}
            onChange={(event) => setSettings({ ...settings, llm_temperature: Number(event.target.value) })}
            className="mt-2 w-full"
          />
        </label>
        <label className="block text-sm">
          Passages récupérés (top-k)
          <input
            type="number"
            min={1}
            max={20}
            value={settings.rag_top_k}
            onChange={(event) => setSettings({ ...settings, rag_top_k: Number(event.target.value) })}
            className="mt-1 w-full rounded-xl border border-line bg-canvas px-3 py-2"
          />
        </label>
        <label className="block text-sm">
          Seuil de pertinence
          <input
            type="number"
            min={0}
            max={1}
            step={0.05}
            value={settings.rag_score_threshold}
            onChange={(event) => setSettings({ ...settings, rag_score_threshold: Number(event.target.value) })}
            className="mt-1 w-full rounded-xl border border-line bg-canvas px-3 py-2"
          />
        </label>
        <Button onClick={() => void save()}>Enregistrer</Button>
        <Button variant="secondary" disabled={diagnosing} onClick={async () => {
          setDiagnosing(true);
          setDiagnosis(null);
          try { setDiagnosis(await api.diagnoseLLM()); }
          catch (error) { setDiagnosis({ ok: false, message: error instanceof Error ? error.message : "Diagnostic impossible." }); }
          finally { setDiagnosing(false); }
        }}>{diagnosing ? "Diagnostic…" : "Tester la connexion IA"}</Button>
        {diagnosis && <p role="status" className={diagnosis.ok ? "text-emerald-600" : "text-red-500"}>{diagnosis.message}</p>}
        <Button
          variant="danger"
          type="button"
          onClick={async () => {
            const result = await api.clearConversations();
            toast.success(`${result.deleted} conversation(s) supprimée(s).`);
          }}
        >
          Effacer l’historique des conversations
        </Button>
      </Card>
      <Card className="space-y-2 text-sm text-muted">
        <p>Application : {settings.app_name} {settings.app_version}</p>
        <p>Embeddings : {settings.embedding_provider} · {settings.embedding_model}</p>
        <p>Clé API présente côté serveur : {settings.has_api_key ? "oui" : "non"}</p>
        <p>LLM réellement configuré : {settings.llm_configured ? "oui" : "non"}</p>
        <p>Taille max d’upload : {settings.max_upload_mb} Mo</p>
        <p>Le thème se change via l’icône soleil/lune. L’historique se gère dans Chat et Documents.</p>
        <p>
          Cette application locale n’a pas d’authentification : elle n’est pas prête pour une exposition publique
          multi-utilisateur.
        </p>
      </Card>
    </div>
  );
}
