import { useState } from "react";
import { Chat } from "./Chat";
import { SoilAdvisory } from "./SoilAdvisory";
import { CropRecommend } from "./CropRecommend";

type Sub = "ai" | "soil" | "crops";

const PILLS: { id: Sub; label: string; icon: string }[] = [
  { id: "ai", label: "Ask AI", icon: "💬" },
  { id: "soil", label: "Soil", icon: "🧪" },
  { id: "crops", label: "Crops", icon: "🌱" },
];

export function Advisory() {
  const [sub, setSub] = useState<Sub>("ai");

  return (
    <div className="flex h-full flex-col">
      <div className="mb-3 flex gap-2">
        {PILLS.map((p) => (
          <button
            key={p.id}
            onClick={() => setSub(p.id)}
            className={`flex-1 rounded-xl py-2 text-sm font-semibold ${
              sub === p.id ? "bg-brand-green text-white" : "bg-white text-slate-500"
            }`}
          >
            {p.icon} {p.label}
          </button>
        ))}
      </div>
      <div className="min-h-0 flex-1">
        {sub === "ai" && <Chat />}
        {sub === "soil" && <SoilAdvisory />}
        {sub === "crops" && <CropRecommend />}
      </div>
    </div>
  );
}
