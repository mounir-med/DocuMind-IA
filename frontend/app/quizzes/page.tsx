"use client";

import { useEffect, useRef, useState } from "react";
import { Sparkles } from "lucide-react";
import { toast } from "sonner";
import { DocumentPicker } from "@/components/documents/DocumentPicker";
import { SourceList } from "@/components/sources/SourceList";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { EmptyState } from "@/components/ui/EmptyState";
import { api } from "@/lib/api";
import type { DocumentItem, QuizQuestion } from "@/lib/types";

export default function QuizzesPage() {
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [selected, setSelected] = useState<string[]>([]);
  const [count, setCount] = useState(5);
  const [level, setLevel] = useState("intermediaire");
  const [questions, setQuestions] = useState<QuizQuestion[]>([]);
  const [notice, setNotice] = useState("");
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);
  const requestVersion = useRef(0);

  useEffect(() => {
    api.documents().then(setDocuments).catch((error) => toast.error(error.message));
  }, []);

  async function generate() {
    if (!selected[0]) return toast.error("Sélectionnez un document.");
    setLoading(true);
    setSubmitted(false);
    setAnswers({});
    setQuestions([]);
    setNotice("");
    const version = ++requestVersion.current;
    const requestedIds = [...selected];
    try {
      const result = await api.quiz(requestedIds[0], count, level, requestedIds);
      if (version !== requestVersion.current) return;
      setQuestions(result.questions);
      setNotice(result.notice ?? "");
    } catch (error) {
      if (version !== requestVersion.current) return;
      toast.error(error instanceof Error ? error.message : "QCM impossible.");
    } finally {
      if (version === requestVersion.current) setLoading(false);
    }
  }

  const score = questions.filter((item) => answers[item.id] === item.correct_choice_id).length;

  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-3xl font-semibold">Générateur de QCM</h1>
        <p className="text-muted">Les questions s’appuient sur les passages récupérés. Une seule bonne réponse.</p>
      </header>
      <Card className="space-y-4">
        <DocumentPicker documents={documents} selected={selected} onChange={(ids) => {
          requestVersion.current += 1;
          setSelected(ids);
          setLoading(false);
          setQuestions([]);
          setNotice("");
          setAnswers({});
          setSubmitted(false);
        }} />
        <div className="flex flex-wrap gap-3">
          <label className="text-sm">
            Nombre
            <input
              type="number"
              min={1}
              max={15}
              value={count}
              onChange={(event) => setCount(Number(event.target.value))}
              className="ml-2 w-20 rounded-lg border border-line bg-surface px-2 py-1"
            />
          </label>
          <select
            value={level}
            onChange={(event) => setLevel(event.target.value)}
            className="rounded-lg border border-line bg-surface px-3 py-1"
          >
            <option value="facile">Facile</option>
            <option value="intermediaire">Intermédiaire</option>
            <option value="avance">Avancé</option>
          </select>
          <Button onClick={() => void generate()} disabled={loading}>
            {loading ? `Génération de ${count} questions…` : "Générer le quiz"}
          </Button>
        </div>
        {loading ? (
          <p role="status" className="text-sm text-muted">
            Le modèle local traite le document. Le délai dépend des performances de l’ordinateur.
          </p>
        ) : null}
      </Card>
      {!questions.length ? (
        <EmptyState icon={Sparkles} title="Pas encore de quiz" description="Sélectionnez des documents indexés pour créer un QCM." />
      ) : (
        <form
          className="space-y-4"
          onSubmit={(event) => {
            event.preventDefault();
            setSubmitted(true);
          }}
        >
          {questions.map((question, index) => (
            <Card key={question.id}>
              <p className="font-medium">
                {index + 1}. {question.question}
              </p>
              <div className="mt-3 space-y-2">
                {question.choices.map((choice) => (
                  <label key={choice.id} className="flex items-center gap-2 text-sm">
                    <input
                      type="radio"
                      name={question.id}
                      value={choice.id}
                      checked={answers[question.id] === choice.id}
                      onChange={() => setAnswers((current) => ({ ...current, [question.id]: choice.id }))}
                    />
                    {choice.text}
                  </label>
                ))}
              </div>
              {submitted ? (
                <div className="mt-3 text-sm">
                  <p className={answers[question.id] === question.correct_choice_id ? "text-green-700" : "text-red-600"}>
                    {answers[question.id] === question.correct_choice_id ? "Bonne réponse." : "Réponse incorrecte."}
                  </p>
                  <p className="mt-1 text-muted">{question.explanation}</p>
                  {question.source ? <div className="mt-3"><SourceList sources={[question.source]} /></div> : null}
                </div>
              ) : null}
            </Card>
          ))}
          <div className="flex gap-2">
            <Button type="submit">Valider</Button>
            <Button
              type="button"
              variant="secondary"
              onClick={() => {
                setAnswers({});
                setSubmitted(false);
              }}
            >
              Recommencer
            </Button>
          </div>
          {submitted ? (
            <p className="text-lg font-semibold">
              Score : {score} / {questions.length}
            </p>
          ) : null}
        </form>
      )}
      {notice && <p role="status" className="text-sm text-muted">{notice}</p>}
    </div>
  );
}
