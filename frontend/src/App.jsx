// frontend/src/App.jsx
import { useEffect, useState } from "react";
import { askShop } from "./api/shop.js";

const AGENTS = [
  { name: "Planner", hint: "Understanding your needs" },
  { name: "Researcher", hint: "Searching products" },
  { name: "Writer", hint: "Drafting the advice" },
  { name: "Critic", hint: "Checking the result" },
];

const EXAMPLES = [
  "I need a laptop for coding, budget 150000 LKR",
  "I need headphones, budget 15000 LKR",
  "I need a mouse, budget 5000 LKR",
];

const formatLkr = (n) => `LKR ${Number(n || 0).toLocaleString("en-LK")}`;

export default function App() {
  const [topic, setTopic] = useState(EXAMPLES[0]);
  const [answer, setAnswer] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState(0);
  const [copied, setCopied] = useState(false);

  // Move the progress indicator through the four agents while waiting.
  useEffect(() => {
    if (!loading) return;
    const id = setInterval(() => setStep((s) => Math.min(s + 1, AGENTS.length - 1)), 2500);
    return () => clearInterval(id);
  }, [loading]);

  async function handleAsk() {
    if (!topic.trim() || loading) return;
    setStep(0);
    setLoading(true);
    setAnswer(null);
    setError("");
    try {
      const data = await askShop(topic);
      setAnswer(data);
    } catch {
      setError("Can't reach the backend. Start it on port 8002, then try again.");
    }
    setLoading(false);
  }

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(answer.recommendation);
      setCopied(true);
      setTimeout(() => setCopied(false), 1800);
    } catch {
      /* clipboard unavailable */
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800">
      {/* Header */}
      <header className="bg-gradient-to-br from-teal-700 via-teal-600 to-emerald-500 pb-24 pt-12 text-white">
        <div className="mx-auto max-w-3xl px-5">
          <div className="flex items-center gap-3">
            <span className="flex h-12 w-12 items-center justify-center rounded-2xl bg-white/20 text-2xl">
              🛒
            </span>
            <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">Shopping Assistant Pro</h1>
          </div>
          <p className="mt-4 max-w-xl text-lg leading-relaxed text-teal-50">
            Tell us what you want to buy and your budget. Four AI agents will research it and
            recommend the best option.
          </p>
          <div className="mt-5 flex flex-wrap gap-2 text-sm">
            {["Pinecone", "MCP", "LangGraph"].map((t) => (
              <span key={t} className="rounded-full bg-white/15 px-3 py-1 font-medium text-white">
                {t}
              </span>
            ))}
          </div>
        </div>
      </header>

      <main className="mx-auto -mt-16 max-w-3xl space-y-6 px-5 pb-16">
        {/* Input card */}
        <section className="rounded-3xl bg-white p-6 shadow-xl shadow-teal-900/10 ring-1 ring-slate-200 sm:p-8">
          <label htmlFor="topic" className="block text-lg font-semibold text-slate-900">
            What do you need?
          </label>
          <textarea
            id="topic"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            onKeyDown={(e) => {
              if ((e.ctrlKey || e.metaKey) && e.key === "Enter") handleAsk();
            }}
            rows={3}
            placeholder="Example: I need a phone for photography, budget 80000 LKR"
            className="mt-3 w-full resize-none rounded-2xl border border-slate-300 bg-slate-50 p-4 text-base leading-relaxed text-slate-900 placeholder:text-slate-400 focus:border-teal-500 focus:bg-white focus:outline-none focus:ring-4 focus:ring-teal-500/20"
          />

          <div className="mt-4">
            <p className="text-sm font-medium text-slate-500">Quick examples</p>
            <div className="mt-2 flex flex-wrap gap-2">
              {EXAMPLES.map((ex) => (
                <button
                  key={ex}
                  type="button"
                  onClick={() => setTopic(ex)}
                  className={`rounded-full border px-4 py-2 text-sm transition focus:outline-none focus-visible:ring-4 focus-visible:ring-teal-500/30 ${
                    topic === ex
                      ? "border-teal-600 bg-teal-50 font-semibold text-teal-800"
                      : "border-slate-300 bg-white text-slate-700 hover:border-teal-400 hover:bg-teal-50"
                  }`}
                >
                  {ex}
                </button>
              ))}
            </div>
          </div>

          <button
            onClick={handleAsk}
            disabled={loading || !topic.trim()}
            className="mt-6 flex w-full items-center justify-center gap-3 rounded-2xl bg-amber-500 px-6 py-4 text-lg font-bold text-slate-900 shadow-lg shadow-amber-500/30 transition hover:bg-amber-400 focus:outline-none focus-visible:ring-4 focus-visible:ring-amber-400/50 disabled:cursor-not-allowed disabled:bg-slate-200 disabled:text-slate-500 disabled:shadow-none"
          >
            {loading ? (
              <>
                <span className="h-5 w-5 animate-spin rounded-full border-2 border-slate-500 border-t-transparent" />
                Working on it...
              </>
            ) : (
              "Get recommendation"
            )}
          </button>
          <p className="mt-2 text-center text-sm text-slate-400">Tip: press Ctrl + Enter to send</p>
        </section>

        {/* Progress */}
        {loading && (
          <section
            aria-live="polite"
            className="rounded-3xl bg-white p-6 shadow-md ring-1 ring-slate-200 sm:p-8"
          >
            <h2 className="text-lg font-semibold text-slate-900">Your team is working</h2>
            <ol className="mt-4 space-y-3">
              {AGENTS.map((a, i) => {
                const done = i < step;
                const active = i === step;
                return (
                  <li key={a.name} className="flex items-center gap-4">
                    <span
                      className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-full text-sm font-bold ${
                        done
                          ? "bg-emerald-500 text-white"
                          : active
                          ? "animate-pulse bg-amber-400 text-slate-900"
                          : "bg-slate-100 text-slate-400"
                      }`}
                    >
                      {done ? "✓" : i + 1}
                    </span>
                    <div>
                      <p className={`font-semibold ${i <= step ? "text-slate-900" : "text-slate-400"}`}>
                        {a.name}
                      </p>
                      <p className={`text-sm ${i <= step ? "text-slate-600" : "text-slate-400"}`}>
                        {a.hint}
                      </p>
                    </div>
                  </li>
                );
              })}
            </ol>
          </section>
        )}

        {/* Error */}
        {error && (
          <section
            role="alert"
            className="flex gap-4 rounded-3xl border border-red-200 bg-red-50 p-6 text-red-900"
          >
            <span className="text-2xl">⚠️</span>
            <div>
              <h2 className="font-semibold">Something went wrong</h2>
              <p className="mt-1 leading-relaxed">{error}</p>
            </div>
          </section>
        )}

        {/* Result */}
        {answer && (
          <section className="overflow-hidden rounded-3xl bg-white shadow-xl shadow-teal-900/10 ring-1 ring-slate-200">
            <div className="flex items-center justify-between gap-3 border-b border-slate-100 bg-emerald-50 px-6 py-4 sm:px-8">
              <h2 className="text-xl font-bold text-emerald-900">Final recommendation</h2>
              <button
                onClick={handleCopy}
                className="rounded-full border border-emerald-300 bg-white px-4 py-1.5 text-sm font-semibold text-emerald-800 transition hover:bg-emerald-100 focus:outline-none focus-visible:ring-4 focus-visible:ring-emerald-400/40"
              >
                {copied ? "Copied" : "Copy"}
              </button>
            </div>

            <div className="px-6 py-6 sm:px-8">
              <p className="whitespace-pre-wrap text-lg leading-8 text-slate-800">
                {answer.recommendation}
              </p>
            </div>

            <dl className="grid grid-cols-2 gap-px border-t border-slate-100 bg-slate-100">
              <div className="bg-white px-6 py-4 sm:px-8">
                <dt className="text-sm text-slate-500">Budget</dt>
                <dd className="mt-1 text-xl font-bold text-teal-700">{formatLkr(answer.budget)}</dd>
              </div>
              <div className="bg-white px-6 py-4 sm:px-8">
                <dt className="text-sm text-slate-500">Attempts</dt>
                <dd className="mt-1 text-xl font-bold text-teal-700">{answer.attempts}</dd>
              </div>
            </dl>
          </section>
        )}
      </main>
    </div>
  );
}