import { useState } from "react";
import { api } from "../api";
import { useApp } from "../store";
import { tr } from "../i18n";
import { Banner, Button, Card, Input } from "../components/ui";

export function Profile() {
  const { lang, farmer, setFarmer, lat, lon, setLocation } = useApp();
  const [area, setArea] = useState("");
  const [msg, setMsg] = useState("");
  const [tone, setTone] = useState<"ok" | "error">("ok");
  const [busy, setBusy] = useState(false);
  const [sosIssue, setSosIssue] = useState("");

  function useGps() {
    if (!navigator.geolocation) {
      setTone("error");
      setMsg("GPS not available in this browser.");
      return;
    }
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setLocation(pos.coords.latitude, pos.coords.longitude);
        setTone("ok");
        setMsg(`Location set: ${pos.coords.latitude.toFixed(4)}, ${pos.coords.longitude.toFixed(4)}`);
      },
      () => {
        setTone("error");
        setMsg("Could not get GPS location (permission denied).");
      }
    );
  }

  async function mapFarm() {
    if (!farmer || !area) return;
    setBusy(true);
    try {
      await api.registerFarm({ phone: farmer.phone, lat, lon, area });
      setTone("ok");
      setMsg("Farm mapped successfully. NDVI will appear on Home once satellite data is ready.");
    } catch (e) {
      setTone("error");
      setMsg((e as Error).message);
    } finally {
      setBusy(false);
    }
  }

  async function sendSos() {
    if (!farmer || !sosIssue.trim()) return;
    setBusy(true);
    try {
      await api.raiseSos({ phone: farmer.phone, issue: sosIssue, lat, lon });
      setTone("ok");
      setMsg("🚨 SOS sent. An officer has been notified.");
      setSosIssue("");
    } catch (e) {
      setTone("error");
      setMsg((e as Error).message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="space-y-3">
      <Card>
        <div className="flex items-center gap-3">
          <div className="flex h-14 w-14 items-center justify-center rounded-full bg-brand-greenLight text-2xl">
            👤
          </div>
          <div>
            <div className="text-lg font-bold text-slate-800">{farmer?.name}</div>
            <div className="text-sm text-slate-500">
              {farmer?.phone} · {farmer?.district || farmer?.village || "—"}
            </div>
          </div>
        </div>
      </Card>

      {msg && <Banner tone={tone}>{msg}</Banner>}

      {/* Farm mapping */}
      <Card className="space-y-3">
        <div className="font-bold text-slate-700">🗺️ Map my farm</div>
        <div className="text-sm text-slate-500">
          Current location: {lat.toFixed(4)}, {lon.toFixed(4)}
        </div>
        <Button variant="ghost" onClick={useGps}>
          📍 Use my GPS location
        </Button>
        <Input
          label="Farm size (acres)"
          inputMode="decimal"
          value={area}
          onChange={(e) => setArea(e.target.value)}
        />
        <Button onClick={mapFarm} disabled={!area || busy}>
          Save farm
        </Button>
      </Card>

      {/* SOS */}
      <Card className="space-y-3 border-l-4 border-l-red-500">
        <div className="font-bold text-red-600">🚨 {tr("sos", lang)}</div>
        <Input
          label="Describe the emergency"
          value={sosIssue}
          onChange={(e) => setSosIssue(e.target.value)}
          placeholder="e.g. Locust swarm near my field"
        />
        <Button variant="danger" onClick={sendSos} disabled={!sosIssue.trim() || busy}>
          Send SOS to officer
        </Button>
      </Card>

      <Button variant="ghost" onClick={() => setFarmer(null)}>
        {tr("logout", lang)}
      </Button>
    </div>
  );
}
