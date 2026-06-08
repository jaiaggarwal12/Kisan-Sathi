import { useEffect, useRef, useState } from "react";
import { api } from "../api";
import { useApp } from "../store";
import { tr } from "../i18n";
import { Banner, Button, Card, Spinner } from "../components/ui";
import { Map } from "../components/Map";

export function Pest() {
  const { lang, farmer, lat, lon } = useApp();
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string>("");
  const [result, setResult] = useState<any>(null);
  const [reports, setReports] = useState<any[]>([]);
  const [clusters, setClusters] = useState<any[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  function loadHeatmap() {
    api.pestHeatmap().then(setReports).catch(() => {});
    api
      .nearbyOutbreaks(lat, lon, 5)
      .then((d) => setClusters(d.clusters || []))
      .catch(() => {});
  }

  useEffect(loadHeatmap, []);

  function onPick(e: React.ChangeEvent<HTMLInputElement>) {
    const f = e.target.files?.[0];
    if (!f) return;
    setFile(f);
    setPreview(URL.createObjectURL(f));
    setResult(null);
  }

  async function detect() {
    if (!file || !farmer) return;
    setBusy(true);
    setError("");
    try {
      const r = await api.reportPest({ phone: farmer.phone, lat, lon }, file);
      setResult(r);
      loadHeatmap();
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }

  const points = reports
    .filter((r) => r.lat && r.lon)
    .map((r) => ({ lat: r.lat, lon: r.lon, label: `${r.pest} (${Math.round(r.confidence * 100)}%)` }));

  return (
    <div className="space-y-3">
      {clusters.length > 0 && (
        <div className="space-y-2">
          {clusters.map((c) => (
            <div
              key={c.pest}
              className="flex items-center gap-3 rounded-2xl border border-red-200 bg-red-50 p-3"
            >
              <span className="text-2xl">⚠️</span>
              <div className="text-sm text-red-800">
                <b>{c.count}</b> farmer(s) within 5 km reported <b>{c.pest}</b> (nearest{" "}
                {c.nearest_km} km). Scout your crop early.
              </div>
            </div>
          ))}
        </div>
      )}

      <Card>
        <input ref={inputRef} type="file" accept="image/*" hidden onChange={onPick} />
        {preview ? (
          <img src={preview} alt="preview" className="mb-3 h-48 w-full rounded-xl object-cover" />
        ) : (
          <button
            onClick={() => inputRef.current?.click()}
            className="mb-3 flex h-48 w-full flex-col items-center justify-center gap-2 rounded-xl border-2 border-dashed border-slate-300 text-slate-400"
          >
            <span className="text-4xl">📷</span>
            <span className="text-sm">{tr("uploadPest", lang)}</span>
          </button>
        )}
        <div className="grid grid-cols-2 gap-2">
          <Button variant="ghost" onClick={() => inputRef.current?.click()}>
            📷 {tr("uploadPest", lang)}
          </Button>
          <Button onClick={detect} disabled={!file || busy}>
            {tr("detect", lang)}
          </Button>
        </div>
      </Card>

      {error && <Banner tone="error">{error}</Banner>}
      {busy && <Spinner label={tr("loading", lang)} />}

      {result && (
        <Card className="border-l-4 border-l-brand-orange">
          <div className="flex items-center justify-between">
            <div className="text-lg font-bold text-slate-800">{result.report.pest}</div>
            <div className="rounded-full bg-brand-greenLight px-2 py-0.5 text-xs font-semibold text-brand-greenDark">
              {Math.round(result.report.confidence * 100)}%
            </div>
          </div>
          <div className="mt-1 text-sm text-slate-600">💊 {result.remedy}</div>
          <div className="mt-2 text-[11px] text-slate-400">Model: {result.model}</div>
        </Card>
      )}

      <div>
        <div className="mb-2 px-1 text-sm font-bold text-slate-600">
          {tr("outbreaks", lang)} ({points.length})
        </div>
        <Card className="p-2">
          <Map points={points} center={[lat, lon]} />
        </Card>
      </div>
    </div>
  );
}
