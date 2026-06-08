import type { ReactNode } from "react";
import { useApp } from "../store";
import { tr, type Lang } from "../i18n";

export type Tab = "home" | "market" | "advisory" | "pest" | "profile";

const TABS: { id: Tab; icon: string; key: string }[] = [
  { id: "home", icon: "🏠", key: "home" },
  { id: "market", icon: "🛒", key: "market" },
  { id: "advisory", icon: "🌱", key: "advisory" },
  { id: "pest", icon: "🐛", key: "pest" },
  { id: "profile", icon: "👤", key: "profile" },
];

const LANGS: { id: Lang; label: string }[] = [
  { id: "en", label: "EN" },
  { id: "hi", label: "हिं" },
  { id: "pa", label: "ਪੰ" },
];

export function Shell({
  tab,
  setTab,
  children,
}: {
  tab: Tab;
  setTab: (t: Tab) => void;
  children: ReactNode;
}) {
  const { lang, setLang, farmer } = useApp();

  return (
    <div className="flex h-full w-full items-center justify-center p-0 sm:p-6">
      {/* Phone frame */}
      <div className="relative flex h-full w-full max-w-[420px] flex-col overflow-hidden bg-slate-50 shadow-2xl sm:h-[860px] sm:rounded-[2.5rem] sm:border-[10px] sm:border-slate-900">
        {/* Header */}
        <header className="bg-brand-green px-5 pb-4 pt-6 text-white">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="text-2xl">🚜</span>
              <div>
                <div className="text-lg font-extrabold leading-none">{tr("appName", lang)}</div>
                <div className="text-[11px] text-green-100">{tr("tagline", lang)}</div>
              </div>
            </div>
            <div className="flex gap-1 rounded-full bg-white/15 p-1">
              {LANGS.map((l) => (
                <button
                  key={l.id}
                  onClick={() => setLang(l.id)}
                  className={`rounded-full px-2 py-0.5 text-xs font-semibold ${
                    lang === l.id ? "bg-white text-brand-green" : "text-white"
                  }`}
                >
                  {l.label}
                </button>
              ))}
            </div>
          </div>
          {farmer && (
            <div className="mt-3 text-sm text-green-50">
              {farmer.name} · {farmer.village || farmer.district || "—"}
            </div>
          )}
        </header>

        {/* Scrollable content */}
        <main className="no-scrollbar flex-1 overflow-y-auto px-4 py-4">{children}</main>

        {/* Bottom nav */}
        <nav className="flex border-t border-slate-200 bg-white">
          {TABS.map((t) => (
            <button
              key={t.id}
              onClick={() => setTab(t.id)}
              className={`flex flex-1 flex-col items-center gap-0.5 py-2.5 text-[11px] font-medium ${
                tab === t.id ? "text-brand-green" : "text-slate-400"
              }`}
            >
              <span className="text-xl">{t.icon}</span>
              {tr(t.key, lang)}
            </button>
          ))}
        </nav>
      </div>
    </div>
  );
}
