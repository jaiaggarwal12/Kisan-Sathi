import { useEffect, useState } from "react";
import { api } from "./api";
import { Map, type MapPoint } from "./components/Map";

interface Summary {
  farmers: number;
  farms: number;
  pest_reports: number;
  open_sos: number;
  pest_breakdown: { pest: string; count: number }[];
}

function StatCard({ label, value, icon, tone }: { label: string; value: number; icon: string; tone: string }) {
  return (
    <div className="flex items-center gap-4 rounded-2xl bg-white p-5 shadow-sm">
      <div className={`flex h-12 w-12 items-center justify-center rounded-xl text-2xl ${tone}`}>{icon}</div>
      <div>
        <div className="text-3xl font-extrabold text-slate-800">{value}</div>
        <div className="text-sm text-slate-500">{label}</div>
      </div>
    </div>
  );
}

export default function App() {
  const [summary, setSummary] = useState<Summary | null>(null);
  const [points, setPoints] = useState<MapPoint[]>([]);
  const [sos, setSos] = useState<any[]>([]);
  const [farmers, setFarmers] = useState<any[]>([]);
  const [error, setError] = useState("");

  async function load() {
    try {
      const [s, farms, pests, sosList, farmerList] = await Promise.all([
        api.summary(),
        api.farms(),
        api.pestHeatmap(),
        api.sos(),
        api.farmers(),
      ]);
      setSummary(s);
      setSos(sosList);
      setFarmers(farmerList);
      const farmPts: MapPoint[] = farms.map((f: any) => ({
        lat: f.lat,
        lon: f.lon,
        kind: "farm" as const,
        label: `<b>${f.name}</b><br/>${f.village || f.district || ""} · ${f.area} acre`,
      }));
      const pestPts: MapPoint[] = pests
        .filter((p: any) => p.lat && p.lon)
        .map((p: any) => ({
          lat: p.lat,
          lon: p.lon,
          kind: "pest" as const,
          label: `<b>${p.pest}</b><br/>${Math.round(p.confidence * 100)}% confidence`,
        }));
      setPoints([...farmPts, ...pestPts]);
    } catch (e) {
      setError((e as Error).message);
    }
  }

  useEffect(() => {
    load();
    const t = setInterval(load, 15000); // auto-refresh every 15s
    return () => clearInterval(t);
  }, []);

  async function resolve(id: number) {
    await api.resolveSos(id);
    load();
  }

  const maxPest = Math.max(1, ...(summary?.pest_breakdown.map((p) => p.count) || [1]));

  return (
    <div className="min-h-full">
      {/* Top bar */}
      <header className="bg-brand-navy px-6 py-4 text-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-2xl">🚜</span>
            <div>
              <div className="text-lg font-extrabold leading-none">Kisan Sathi</div>
              <div className="text-xs text-slate-300">Agriculture Officer Portal</div>
            </div>
          </div>
          <div className="text-sm text-slate-300">District control center · auto-refresh 15s</div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl space-y-6 p-6">
        {error && <div className="rounded-xl bg-red-50 px-4 py-3 text-red-700">{error}</div>}

        {/* Stat cards */}
        <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
          <StatCard label="Registered farmers" value={summary?.farmers ?? 0} icon="👨‍🌾" tone="bg-green-100" />
          <StatCard label="Mapped farms" value={summary?.farms ?? 0} icon="🌾" tone="bg-lime-100" />
          <StatCard label="Pest reports" value={summary?.pest_reports ?? 0} icon="🐛" tone="bg-orange-100" />
          <StatCard label="Open SOS" value={summary?.open_sos ?? 0} icon="🚨" tone="bg-red-100" />
        </div>

        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          {/* Map */}
          <div className="lg:col-span-2">
            <div className="rounded-2xl bg-white p-3 shadow-sm">
              <div className="mb-2 flex items-center justify-between px-1">
                <h2 className="font-bold text-slate-700">Farms & pest outbreaks</h2>
                <div className="flex gap-3 text-xs text-slate-500">
                  <span>🟢 Farm</span>
                  <span>🔴 Pest report</span>
                </div>
              </div>
              <div className="h-[440px] overflow-hidden rounded-xl">
                <Map points={points} />
              </div>
            </div>
          </div>

          {/* SOS panel */}
          <div className="rounded-2xl bg-white p-4 shadow-sm">
            <h2 className="mb-3 font-bold text-slate-700">🚨 SOS alerts</h2>
            <div className="space-y-2">
              {sos.length === 0 && <div className="text-sm text-slate-400">No alerts.</div>}
              {sos.map((a) => (
                <div
                  key={a.id}
                  className={`rounded-xl border p-3 ${
                    a.status === "open" ? "border-red-200 bg-red-50" : "border-slate-200 bg-slate-50"
                  }`}
                >
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <div className="text-sm font-semibold text-slate-800">{a.issue}</div>
                      <div className="text-xs text-slate-500">📞 {a.farmer_phone}</div>
                    </div>
                    {a.status === "open" ? (
                      <button
                        onClick={() => resolve(a.id)}
                        className="shrink-0 rounded-lg bg-brand-green px-3 py-1 text-xs font-semibold text-white"
                      >
                        Resolve
                      </button>
                    ) : (
                      <span className="shrink-0 text-xs font-semibold text-green-600">✓ Resolved</span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          {/* Pest breakdown */}
          <div className="rounded-2xl bg-white p-4 shadow-sm">
            <h2 className="mb-3 font-bold text-slate-700">Pest breakdown</h2>
            {summary?.pest_breakdown.length ? (
              <div className="space-y-2">
                {summary.pest_breakdown.map((p) => (
                  <div key={p.pest}>
                    <div className="flex justify-between text-sm text-slate-600">
                      <span>{p.pest}</span>
                      <span className="font-semibold">{p.count}</span>
                    </div>
                    <div className="h-2 rounded-full bg-slate-100">
                      <div
                        className="h-2 rounded-full bg-brand-orange"
                        style={{ width: `${(p.count / maxPest) * 100}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-sm text-slate-400">No pest reports yet.</div>
            )}
          </div>

          {/* Farmer table */}
          <div className="rounded-2xl bg-white p-4 shadow-sm lg:col-span-2">
            <h2 className="mb-3 font-bold text-slate-700">Registered farmers</h2>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead>
                  <tr className="text-slate-400">
                    <th className="pb-2">Name</th>
                    <th className="pb-2">Phone</th>
                    <th className="pb-2">District</th>
                    <th className="pb-2">State</th>
                  </tr>
                </thead>
                <tbody>
                  {farmers.map((f) => (
                    <tr key={f.phone} className="border-t border-slate-100">
                      <td className="py-2 font-medium text-slate-700">{f.name}</td>
                      <td className="py-2 text-slate-500">{f.phone}</td>
                      <td className="py-2 text-slate-500">{f.district || "—"}</td>
                      <td className="py-2 text-slate-500">{f.state || "—"}</td>
                    </tr>
                  ))}
                  {farmers.length === 0 && (
                    <tr>
                      <td colSpan={4} className="py-4 text-center text-slate-400">
                        No farmers registered yet.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
