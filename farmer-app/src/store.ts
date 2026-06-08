import { createContext, createElement, useContext, useEffect, useState, type ReactNode } from "react";
import type { Lang } from "./i18n";

export interface Farmer {
  phone: string;
  name: string;
  village?: string;
  district?: string;
  state?: string;
  language?: string;
}

interface AppState {
  farmer: Farmer | null;
  setFarmer: (f: Farmer | null) => void;
  lang: Lang;
  setLang: (l: Lang) => void;
  // A default location (Patiala, Punjab) used for weather until a farm is mapped.
  lat: number;
  lon: number;
  setLocation: (lat: number, lon: number) => void;
}

const Ctx = createContext<AppState | undefined>(undefined);

export function AppProvider({ children }: { children: ReactNode }) {
  const [farmer, setFarmerState] = useState<Farmer | null>(null);
  const [lang, setLangState] = useState<Lang>("en");
  const [lat, setLat] = useState(30.3548);
  const [lon, setLon] = useState(76.3649);

  // Restore session from localStorage.
  useEffect(() => {
    const saved = localStorage.getItem("ks_farmer");
    if (saved) setFarmerState(JSON.parse(saved));
    const savedLang = localStorage.getItem("ks_lang") as Lang | null;
    if (savedLang) setLangState(savedLang);
  }, []);

  const setFarmer = (f: Farmer | null) => {
    setFarmerState(f);
    if (f) localStorage.setItem("ks_farmer", JSON.stringify(f));
    else localStorage.removeItem("ks_farmer");
  };

  const setLang = (l: Lang) => {
    setLangState(l);
    localStorage.setItem("ks_lang", l);
  };

  const setLocation = (la: number, lo: number) => {
    setLat(la);
    setLon(lo);
  };

  return createElement(
    Ctx.Provider,
    { value: { farmer, setFarmer, lang, setLang, lat, lon, setLocation } },
    children
  );
}

export function useApp() {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error("useApp must be used within AppProvider");
  return ctx;
}
