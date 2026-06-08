import { useEffect, useRef } from "react";
import L from "leaflet";

export interface MapPoint {
  lat: number;
  lon: number;
  label: string;
  kind: "farm" | "pest";
}

// Leaflet map used directly (no react-leaflet) to avoid version mismatches.
export function Map({ points }: { points: MapPoint[] }) {
  const ref = useRef<HTMLDivElement>(null);
  const mapRef = useRef<L.Map | null>(null);
  const layerRef = useRef<L.LayerGroup | null>(null);

  useEffect(() => {
    if (!ref.current || mapRef.current) return;
    const map = L.map(ref.current).setView([30.7, 76.0], 7); // North India
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "© OpenStreetMap",
    }).addTo(map);
    layerRef.current = L.layerGroup().addTo(map);
    mapRef.current = map;
    return () => {
      map.remove();
      mapRef.current = null;
    };
  }, []);

  useEffect(() => {
    const layer = layerRef.current;
    const map = mapRef.current;
    if (!layer || !map) return;
    layer.clearLayers();
    const bounds: [number, number][] = [];
    points.forEach((p) => {
      const isPest = p.kind === "pest";
      L.circleMarker([p.lat, p.lon], {
        radius: isPest ? 9 : 7,
        color: isPest ? "#dc2626" : "#15803d",
        fillColor: isPest ? "#ef4444" : "#22c55e",
        fillOpacity: 0.6,
        weight: 2,
      })
        .bindPopup(p.label)
        .addTo(layer);
      bounds.push([p.lat, p.lon]);
    });
    if (bounds.length) map.fitBounds(bounds, { padding: [40, 40], maxZoom: 11 });
  }, [points]);

  return <div ref={ref} className="h-full min-h-[420px] w-full" />;
}
