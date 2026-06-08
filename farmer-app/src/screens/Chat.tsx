import { useRef, useState } from "react";
import { api } from "../api";
import { useApp } from "../store";
import { canListen, listen, speak } from "../voice";

interface Msg {
  from: "user" | "bot";
  text: string;
  reasoning?: string[];
  actions?: string[];
}

const SUGGESTIONS = [
  "How much urea for my wheat?",
  "Should I irrigate today?",
  "Which crop should I grow?",
  "What is the weather at my farm?",
];

export function Chat() {
  const { farmer, lang } = useApp();
  const [messages, setMessages] = useState<Msg[]>([
    { from: "bot", text: "Namaste! Ask me about fertilizer, irrigation, weather, pests, prices or schemes." },
  ]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [listening, setListening] = useState(false);
  const endRef = useRef<HTMLDivElement>(null);

  async function send(text: string) {
    if (!text.trim() || !farmer) return;
    setMessages((m) => [...m, { from: "user", text }]);
    setInput("");
    setBusy(true);
    try {
      const r = await api.chat(farmer.phone, text);
      const botMsg: Msg = { from: "bot", text: r.reply, reasoning: r.reasoning, actions: r.actions };
      setMessages((m) => [...m, botMsg]);
      speak(r.reply, lang);
    } catch (e) {
      setMessages((m) => [...m, { from: "bot", text: (e as Error).message }]);
    } finally {
      setBusy(false);
      setTimeout(() => endRef.current?.scrollIntoView({ behavior: "smooth" }), 50);
    }
  }

  function micPress() {
    if (!canListen()) {
      alert("Voice input isn't supported in this browser. Try Chrome.");
      return;
    }
    setListening(true);
    listen(
      lang,
      (text) => send(text),
      () => setListening(false)
    );
  }

  return (
    <div className="flex h-full flex-col">
      <div className="flex-1 space-y-3 overflow-y-auto pb-2">
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.from === "user" ? "justify-end" : "justify-start"}`}>
            <div
              className={`max-w-[85%] rounded-2xl px-4 py-2.5 text-sm ${
                m.from === "user"
                  ? "bg-brand-green text-white"
                  : "bg-white text-slate-800 shadow-sm"
              }`}
            >
              <div className="flex items-start gap-2">
                <span>{m.text}</span>
                {m.from === "bot" && (
                  <button onClick={() => speak(m.text, lang)} title="Listen" className="shrink-0 text-base">
                    🔊
                  </button>
                )}
              </div>
              {m.reasoning && m.reasoning.length > 0 && (
                <ul className="mt-2 space-y-0.5 rounded-lg bg-amber-50 p-2 text-xs text-amber-800">
                  {m.reasoning.map((r, j) => (
                    <li key={j}>• {r}</li>
                  ))}
                </ul>
              )}
              {m.actions && m.actions.length > 0 && (
                <ul className="mt-1 space-y-0.5 text-xs text-brand-green">
                  {m.actions.map((a, j) => (
                    <li key={j}>👉 {a}</li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        ))}
        {busy && <div className="text-sm text-slate-400">typing…</div>}
        <div ref={endRef} />
      </div>

      {/* Suggestion chips */}
      <div className="flex flex-wrap gap-2 py-2">
        {SUGGESTIONS.map((s) => (
          <button
            key={s}
            onClick={() => send(s)}
            className="rounded-full bg-brand-greenLight px-3 py-1 text-xs font-medium text-brand-greenDark"
          >
            {s}
          </button>
        ))}
      </div>

      {/* Input row */}
      <div className="flex items-center gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send(input)}
          placeholder="Type your question…"
          className="flex-1 rounded-full border border-slate-200 px-4 py-3 text-sm outline-none focus:border-brand-green"
        />
        <button
          onClick={micPress}
          className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-full text-xl ${
            listening ? "animate-pulse bg-red-500 text-white" : "bg-slate-100"
          }`}
        >
          🎤
        </button>
        <button
          onClick={() => send(input)}
          disabled={busy}
          className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-brand-green text-xl text-white"
        >
          ➤
        </button>
      </div>
    </div>
  );
}
