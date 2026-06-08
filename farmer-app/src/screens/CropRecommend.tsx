import { useState } from "react";
import { api } from "../api";
import { useApp } from "../store";
import { Banner, Button, Card, Spinner } from "../components/ui";

export function CropRecommend() {
  const { farmer } = useApp();
  const [data, setData] = useState<any>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function load() {
    if (!farmer) return;
    setBusy(true);
    setError("");
    try {
      setData(await api.recommend(farmer.phone));
    } catch (e) {
      setError((e as Error).message + " (add a soil test first in the Soil tab)");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="space-y-3">
      <Card>
        <div className="font-bold text-slate-700">🌱 Best crops for your soil</div>
        <p className="mt-1 text-sm text-slate-500">
          Uses your latest soil test and the current sowing season.
        </p>
        <div className="mt-3">
          <Button onClick={load} disabled={busy}>
            Recommend crops
          </Button>
        </div>
      </Card>

      {error && <Banner tone="error">{error}</Banner>}
      {busy && <Spinner />}

      {data && (
        <>
          <Banner tone="info">Season: {data.season}</Banner>
          {data.recommendations.map((r: any, i: number) => (
            <Card key={r.crop} className={i === 0 ? "border-l-4 border-l-brand-green" : ""}>
              <div className="flex items-center justify-between">
                <div className="font-semibold text-slate-800">
                  {i === 0 ? "⭐ " : ""}
                  {r.crop}
                </div>
                <div className="text-sm font-bold text-brand-greenDark">{r.score}/8</div>
              </div>
              <ul className="mt-1 space-y-0.5">
                {r.reasons.map((reason: string, j: number) => (
                  <li key={j} className="text-xs text-slate-500">
                    • {reason}
                  </li>
                ))}
              </ul>
            </Card>
          ))}
        </>
      )}
    </div>
  );
}
