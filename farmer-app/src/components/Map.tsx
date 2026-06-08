import { useEffect, useRef } from "react";
import L from "leaflet";

interface Point {
  lat: number;
  lon: number;
  label: string;
}

// Lightweight Leaflet map (used directly to avoid react-leaflet version churn).
export function Map({ points, center }: { points: Point[]; center: [number, number] }) {
  const ref = useRef<HTMLDivElement>(null);
  const mapRef = useRef<L.Map | null>(null);
  const layerRef = useRef<L.LayerGroup | null>(null);

  useEffect(() => {
    if (!ref.current || mapRef.current) return;
    const map = L.map(ref.current).setView(center, 11);
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
    if (!layer) return;
    layer.clearLayers();
    points.forEach((p) => {
      L.circleMarker([p.lat, p.lon], {
        radius: 10,
        color: "#dc2626",
        fillColor: "#ef4444",
        fillOpacity: 0.5,
        weight: 2,
      })
        .bindPopup(p.label)
        .addTo(layer);
    });
  }, [points]);

  return <div ref={ref} className="h-64 w-full overflow-hidden rounded-xl" />;
}
