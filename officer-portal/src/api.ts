const BASE = import.meta.env.VITE_API_BASE ?? "/api";

async function get(path: string) {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) throw new Error(`Request failed (${res.status})`);
  return res.json();
}

export const api = {
  summary: () => get("/officer/summary"),
  farms: () => get("/officer/farms"),
  farmers: () => get("/farmers"),
  pestHeatmap: () => get("/pest/heatmap?limit=200"),
  sos: () => get("/sos"),
  resolveSos: (id: number) =>
    fetch(`${BASE}/sos/${id}/resolve`, { method: "PATCH" }).then((r) => r.json()),
};
