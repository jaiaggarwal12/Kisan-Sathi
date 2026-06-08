// Thin wrapper around the Kisan Sathi FastAPI backend.
// In dev, Vite proxies /api -> http://127.0.0.1:8000 (see vite.config.ts).
// In production, set VITE_API_BASE to your deployed backend URL.

const BASE = import.meta.env.VITE_API_BASE ?? "/api";

async function handle(res: Response) {
  if (!res.ok) {
    let detail = `Request failed (${res.status})`;
    try {
      const body = await res.json();
      detail = body.detail || detail;
    } catch {
      /* ignore */
    }
    throw new Error(detail);
  }
  return res.json();
}

function form(data: Record<string, string | number | undefined>) {
  const fd = new FormData();
  Object.entries(data).forEach(([k, v]) => {
    if (v !== undefined && v !== "") fd.append(k, String(v));
  });
  return fd;
}

export const api = {
  health: () => fetch(`${BASE}/health`).then(handle),

  registerFarmer: (data: Record<string, string>) =>
    fetch(`${BASE}/farmers/register`, { method: "POST", body: form(data) }).then(handle),

  getFarmer: (phone: string) => fetch(`${BASE}/farmers/${phone}`).then(handle),

  registerFarm: (data: Record<string, string | number>) =>
    fetch(`${BASE}/farms/register`, { method: "POST", body: form(data) }).then(handle),

  registerSoil: (data: Record<string, string | number>) =>
    fetch(`${BASE}/soil/register`, { method: "POST", body: form(data) }).then(handle),

  soilAdvisory: (phone: string, crop: string) =>
    fetch(`${BASE}/soil/advisory/${phone}?crop=${encodeURIComponent(crop)}`).then(handle),

  weather: (lat: number, lon: number) =>
    fetch(`${BASE}/weather/${lat}/${lon}`).then(handle),

  ndviByFarmer: (phone: string) => fetch(`${BASE}/ndvi/farmer/${phone}`).then(handle),

  commodities: () => fetch(`${BASE}/mandi/commodities`).then(handle),
  states: (c: string) => fetch(`${BASE}/mandi/states/${encodeURIComponent(c)}`).then(handle),
  districts: (c: string, s: string) =>
    fetch(`${BASE}/mandi/districts/${encodeURIComponent(c)}/${encodeURIComponent(s)}`).then(handle),
  markets: (c: string, s: string, d: string) =>
    fetch(
      `${BASE}/mandi/markets/${encodeURIComponent(c)}/${encodeURIComponent(s)}/${encodeURIComponent(d)}`
    ).then(handle),
  prices: (c: string, s?: string, d?: string, m?: string) => {
    const q = new URLSearchParams();
    if (s) q.set("state", s);
    if (d) q.set("district", d);
    if (m) q.set("market", m);
    return fetch(`${BASE}/mandi/prices/${encodeURIComponent(c)}?${q}`).then(handle);
  },

  schemes: (phone: string) => fetch(`${BASE}/schemes/eligible/${phone}`).then(handle),

  reportPest: (data: Record<string, string | number>, file: File) => {
    const fd = form(data);
    fd.append("file", file);
    return fetch(`${BASE}/pest/report`, { method: "POST", body: fd }).then(handle);
  },
  pestHeatmap: () => fetch(`${BASE}/pest/heatmap`).then(handle),

  nearbyOutbreaks: (lat: number, lon: number, radiusKm = 5) =>
    fetch(`${BASE}/pest/nearby?lat=${lat}&lon=${lon}&radius_km=${radiusKm}`).then(handle),

  raiseSos: (data: Record<string, string | number>) =>
    fetch(`${BASE}/sos`, { method: "POST", body: form(data) }).then(handle),

  // --- Innovative features ---
  chat: (phone: string, message: string) =>
    fetch(`${BASE}/advisor/chat`, { method: "POST", body: form({ phone, message }) }).then(handle),
  recommend: (phone: string) => fetch(`${BASE}/advisor/recommend/${phone}`).then(handle),
  advisorCrops: () => fetch(`${BASE}/advisor/crops`).then(handle),
  cropCalendar: (crop: string, sowingDate?: string) => {
    const q = sowingDate ? `?sowing_date=${sowingDate}` : "";
    return fetch(`${BASE}/advisor/calendar/${encodeURIComponent(crop)}${q}`).then(handle);
  },
  bestMandi: (commodity: string, state?: string) => {
    const q = state ? `?state=${encodeURIComponent(state)}` : "";
    return fetch(`${BASE}/mandi/best/${encodeURIComponent(commodity)}${q}`).then(handle);
  },
  profit: (crop: string, area: number, state?: string) => {
    const q = new URLSearchParams({ area: String(area) });
    if (state) q.set("state", state);
    return fetch(`${BASE}/mandi/profit/${encodeURIComponent(crop)}?${q}`).then(handle);
  },
};
