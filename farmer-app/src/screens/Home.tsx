import { useEffect, useState } from "react";
import { api } from "../api";
import { useApp } from "../store";
import { tr } from "../i18n";
import { Card, Spinner, Banner } from "../components/ui";

const CAL_CROPS = ["Wheat", "Paddy", "Maize", "Cotton", "Sugarcane", "Mustard"];

export function Home() {
  const { lang, lat, lon, farmer } = useApp();
  const [weather, setWeather] = useState<any>(null);
  const [ndvi, setNdvi] = useState<any>(null);
  const [schemes, setSchemes] = useState<any[]>([]);
  const [calCrop, setCalCrop] = useState("Wheat");
  const [calendar, setCalendar] = useState<any>(null);
  const [wErr, setWErr] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;
    (async () => {
      setLoading(true);
      try {
        const w = await api.weather(lat, lon);
        if (active) setWeather(w);
      } catch (e) {
        if (active) setWErr((e as Error).message);
      }
      try {
        if (farmer) {
          const n = await api.ndviByFarmer(farmer.phone);
          if (active) setNdvi(n);
        }
      } catch {
        /* NDVI may not be ready -> ignore silently */
      }
      try {
        if (farmer) {
          const s = await api.schemes(farmer.phone);
          if (active) setSchemes(s.eligible_schemes || []);
        }
      } catch {
        /* ignore */
      }
      if (active) setLoading(false);
    })();
    return () => {
      active = false;
    };
  }, [lat, lon, farmer]);

  useEffect(() => {
    api.cropCalendar(calCrop).then(setCalendar).catch(() => setCalendar(null));
  }, [calCrop]);

  if (loading) return <Spinner label={tr("loading", lang)} />;

  return (
    <div className="space-y-4">
      {/* Weather card */}
      <Card className="bg-gradient-to-br from-sky-500 to-sky-700 text-white border-0">
        <div className="flex items-center justify-between">
          <div>
            <div className="text-sm text-sky-100">{tr("weather", lang)}</div>
            {weather ? (
              <>
                <div className="text-4xl font-extrabold">{Math.round(weather.temperature)}°C</div>
                <div className="text-sm capitalize text-sky-100">
                  {weather.description} · {weather.location}
                </div>
              </>
            ) : (
              <div className="text-sm">{wErr || "—"}</div>
            )}
          </div>
          <div className="text-5xl">🌤️</div>
        </div>
        {weather?.advisory && (
          <div className="mt-3 rounded-xl bg-white/15 px-3 py-2 text-sm">💡 {weather.advisory}</div>
        )}
      </Card>

      {/* NDVI card */}
      <Card>
        <div className="flex items-center justify-between">
          <div>
            <div className="text-sm font-semibold text-slate-500">{tr("cropHealth", lang)}</div>
            {ndvi ? (
              <>
                <div className="text-2xl font-bold text-brand-greenDark">
                  {ndvi.ndvi_mean != null ? ndvi.ndvi_mean.toFixed(2) : "—"}
                </div>
                <div className="text-sm text-slate-500">{ndvi.health}</div>
              </>
            ) : (
              <div className="text-sm text-slate-400">
                Satellite pass pending — map your farm to enable.
              </div>
            )}
          </div>
          <div className="text-4xl">🛰️</div>
        </div>
        {ndvi?.image_url && (
          <img src={ndvi.image_url} alt="NDVI" className="mt-3 w-full rounded-xl" />
        )}
      </Card>

      {/* Krishi Diary (crop calendar) */}
      <Card>
        <div className="mb-2 flex items-center justify-between">
          <div className="text-sm font-bold text-slate-600">📅 Krishi Diary</div>
          <select
            value={calCrop}
            onChange={(e) => setCalCrop(e.target.value)}
            className="rounded-lg border border-slate-200 bg-white px-2 py-1 text-sm"
          >
            {CAL_CROPS.map((c) => (
              <option key={c}>{c}</option>
            ))}
          </select>
        </div>
        {calendar?.next_task ? (
          <div className="rounded-xl bg-brand-greenLight p-3">
            <div className="text-xs font-semibold text-brand-greenDark">
              Next: {calendar.next_task.date}
              {calendar.next_task.days_away >= 0
                ? ` (in ${calendar.next_task.days_away} days)`
                : ""}
            </div>
            <div className="mt-0.5 text-sm text-slate-700">{calendar.next_task.task}</div>
          </div>
        ) : (
          <div className="text-sm text-slate-400">Select a crop to see its schedule.</div>
        )}
        {calendar && (
          <div className="mt-2 text-xs text-slate-400">
            Sown {calendar.sowing_date} · harvest ~{calendar.harvest_date}
          </div>
        )}
      </Card>

      {/* Schemes */}
      <div>
        <div className="mb-2 px-1 text-sm font-bold text-slate-600">{tr("schemes", lang)}</div>
        {schemes.length === 0 ? (
          <Banner tone="info">No matched schemes yet.</Banner>
        ) : (
          <div className="space-y-2">
            {schemes.slice(0, 3).map((s) => (
              <Card key={s.name} className="border-l-4 border-l-brand-orange">
                <div className="font-semibold text-slate-800">{s.name}</div>
                <div className="text-sm text-slate-500">{s.benefit}</div>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
