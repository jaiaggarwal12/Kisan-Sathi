import { useEffect, useState } from "react";
import { api } from "../api";
import { useApp } from "../store";
import { tr } from "../i18n";
import { Banner, Card, Select, Spinner } from "../components/ui";

// Cascading dropdowns: commodity -> state -> district -> market -> prices.
// Each level only offers options that actually have data today.
export function Market() {
  const { lang } = useApp();
  const [commodities, setCommodities] = useState<string[]>([]);
  const [states, setStates] = useState<string[]>([]);
  const [districts, setDistricts] = useState<string[]>([]);
  const [markets, setMarkets] = useState<string[]>([]);

  const [commodity, setCommodity] = useState("");
  const [state, setState] = useState("");
  const [district, setDistrict] = useState("");
  const [market, setMarket] = useState("");

  const [prices, setPrices] = useState<any[]>([]);
  const [best, setBest] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    setLoading(true);
    api
      .commodities()
      .then((d) => setCommodities(d.commodities || []))
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  async function onCommodity(c: string) {
    setCommodity(c);
    setState(""); setDistrict(""); setMarket("");
    setStates([]); setDistricts([]); setMarkets([]); setPrices([]);
    if (!c) return;
    setLoading(true);
    try {
      const d = await api.states(c);
      setStates(d.states || []);
    } catch (e) { setError((e as Error).message); } finally { setLoading(false); }
  }

  async function onState(s: string) {
    setState(s);
    setDistrict(""); setMarket("");
    setDistricts([]); setMarkets([]);
    if (!s) return;
    setLoading(true);
    try {
      const d = await api.districts(commodity, s);
      setDistricts(d.districts || []);
    } catch (e) { setError((e as Error).message); } finally { setLoading(false); }
  }

  async function onDistrict(d: string) {
    setDistrict(d);
    setMarket("");
    setMarkets([]);
    if (!d) return;
    setLoading(true);
    try {
      const r = await api.markets(commodity, state, d);
      setMarkets(r.markets || []);
    } catch (e) { setError((e as Error).message); } finally { setLoading(false); }
  }

  async function loadPrices(m?: string) {
    setMarket(m || "");
    setLoading(true);
    setError("");
    try {
      const r = await api.prices(commodity, state, district, m);
      setPrices(r.markets || []);
      // Best-mandi insight across the selected state.
      try {
        const b = await api.bestMandi(commodity, state || undefined);
        setBest(b.best ? b : null);
      } catch {
        setBest(null);
      }
    } catch (e) { setError((e as Error).message); } finally { setLoading(false); }
  }

  return (
    <div className="space-y-3">
      <Card className="space-y-3">
        <Select
          label={tr("selectCommodity", lang)}
          options={commodities}
          value={commodity}
          placeholder={tr("selectCommodity", lang)}
          onChange={(e) => onCommodity(e.target.value)}
        />
        <Select
          label={tr("selectState", lang)}
          options={states}
          value={state}
          disabled={!commodity}
          placeholder={tr("selectState", lang)}
          onChange={(e) => onState(e.target.value)}
        />
        <Select
          label={tr("selectDistrict", lang)}
          options={districts}
          value={district}
          disabled={!state}
          placeholder={tr("selectDistrict", lang)}
          onChange={(e) => onDistrict(e.target.value)}
        />
        <Select
          label={tr("selectMarket", lang)}
          options={markets}
          value={market}
          disabled={!district}
          placeholder={tr("selectMarket", lang)}
          onChange={(e) => loadPrices(e.target.value)}
        />
      </Card>

      {error && <Banner tone="error">{error}</Banner>}
      {loading && <Spinner label={tr("loading", lang)} />}

      {best && (
        <Card className="border-0 bg-gradient-to-br from-brand-orange to-amber-600 text-white">
          <div className="text-sm font-semibold text-amber-100">💡 Best place to sell</div>
          <div className="mt-1 text-lg font-bold">
            {best.best.market}, {best.best.district}
          </div>
          <div className="text-sm text-amber-50">
            ₹{best.best.modal_price}/qtl · about ₹{Math.round(best.extra_income_per_quintal)} more
            than the average mandi
          </div>
        </Card>
      )}

      {prices.map((p, i) => (
        <Card key={i} className="border-l-4 border-l-brand-green">
          <div className="flex items-center justify-between">
            <div>
              <div className="font-semibold text-slate-800">
                {p.commodity} {p.variety ? `· ${p.variety}` : ""}
              </div>
              <div className="text-sm text-slate-500">
                {p.market}, {p.district}
              </div>
            </div>
            <div className="text-right">
              <div className="text-lg font-bold text-brand-greenDark">₹{p.modal_price}</div>
              <div className="text-xs text-slate-400">
                ₹{p.min_price}–{p.max_price}/qtl
              </div>
            </div>
          </div>
        </Card>
      ))}
    </div>
  );
}
