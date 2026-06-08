import { useState } from "react";
import { api } from "../api";
import { useApp } from "../store";
import { tr } from "../i18n";
import { Banner, Button, Card, Input, Spinner } from "../components/ui";

const CROPS = ["Wheat", "Paddy", "Maize", "Cotton", "Sugarcane", "Mustard"];

export function SoilAdvisory() {
  const { lang, farmer } = useApp();
  const [form, setForm] = useState({ N: "", P: "", K: "", pH: "", OC: "", EC: "" });
  const [crop, setCrop] = useState("Wheat");
  const [advisory, setAdvisory] = useState<any>(null);
  const [showWhy, setShowWhy] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const set = (k: string, v: string) => setForm((f) => ({ ...f, [k]: v }));

  async function submit() {
    if (!farmer) return;
    setBusy(true);
    setError("");
    try {
      await api.registerSoil({
        phone: farmer.phone,
        N: form.N || 0,
        P: form.P || 0,
        K: form.K || 0,
        pH: form.pH || 7,
        OC: form.OC || 0,
        EC: form.EC || 0,
      });
      const adv = await api.soilAdvisory(farmer.phone, crop);
      setAdvisory(adv);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="space-y-3">
      <Card>
        <div className="mb-2 font-bold text-slate-700">{tr("fertilizerAdvice", lang)}</div>
        <div className="grid grid-cols-3 gap-2">
          <Input label="N" inputMode="numeric" value={form.N} onChange={(e) => set("N", e.target.value)} />
          <Input label="P" inputMode="numeric" value={form.P} onChange={(e) => set("P", e.target.value)} />
          <Input label="K" inputMode="numeric" value={form.K} onChange={(e) => set("K", e.target.value)} />
          <Input label="pH" inputMode="decimal" value={form.pH} onChange={(e) => set("pH", e.target.value)} />
          <Input label="OC %" inputMode="decimal" value={form.OC} onChange={(e) => set("OC", e.target.value)} />
          <Input label="EC" inputMode="decimal" value={form.EC} onChange={(e) => set("EC", e.target.value)} />
        </div>
        <label className="mt-3 block">
          <span className="text-sm font-medium text-slate-600">Crop</span>
          <select
            value={crop}
            onChange={(e) => setCrop(e.target.value)}
            className="mt-1 w-full rounded-xl border border-slate-200 bg-white px-4 py-3"
          >
            {CROPS.map((c) => (
              <option key={c}>{c}</option>
            ))}
          </select>
        </label>
        <div className="mt-3">
          <Button onClick={submit} disabled={busy}>
            {tr("detect", lang)}
          </Button>
        </div>
      </Card>

      {error && <Banner tone="error">{error}</Banner>}
      {busy && <Spinner label={tr("loading", lang)} />}

      {advisory && (
        <Card className="border-l-4 border-l-brand-green">
          <div className="mb-2 font-bold text-brand-greenDark">{advisory.crop} — recommendations</div>
          <ul className="space-y-1">
            {advisory.recommendations.map((r: string, i: number) => (
              <li key={i} className="flex gap-2 text-sm text-slate-700">
                <span>✅</span> {r}
              </li>
            ))}
          </ul>
          <button onClick={() => setShowWhy((v) => !v)} className="mt-3 text-sm font-semibold text-brand-orange">
            {showWhy ? "▲" : "▼"} {tr("whyThis", lang)}
          </button>
          {showWhy && (
            <ul className="mt-2 space-y-1 rounded-xl bg-amber-50 p-3">
              {advisory.explanation.map((r: string, i: number) => (
                <li key={i} className="text-xs text-amber-800">
                  • {r}
                </li>
              ))}
            </ul>
          )}
        </Card>
      )}
    </div>
  );
}
