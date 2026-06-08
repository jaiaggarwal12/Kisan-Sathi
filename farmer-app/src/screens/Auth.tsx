import { useState } from "react";
import { api } from "../api";
import { useApp } from "../store";
import { tr } from "../i18n";
import { Banner, Button, Input, Select } from "../components/ui";
import { STATES_DISTRICTS, STATE_LIST } from "../data/locations";

// Simple OTP-style login. The backend doesn't send a real SMS in this build,
// so we use a demo OTP (1234). Swap in Twilio Verify later without UI changes.
const DEMO_OTP = "1234";

export function Auth() {
  const { lang, setFarmer, setLocation } = useApp();
  const [step, setStep] = useState<"phone" | "otp" | "profile">("phone");
  const [phone, setPhone] = useState("");
  const [otp, setOtp] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  // profile fields
  const [name, setName] = useState("");
  const [village, setVillage] = useState("");
  const [district, setDistrict] = useState("");
  const [state, setState] = useState("Punjab");

  // Resolve the farmer's district/state to coordinates so the dashboard shows
  // weather for THEIR place, not a default. Failures are non-fatal.
  async function applyLocation(districtName?: string, stateName?: string) {
    const place = [districtName, stateName].filter(Boolean).join(",");
    if (!place) return;
    try {
      const geo = await api.geocode(place);
      if (geo?.lat != null && geo?.lon != null) setLocation(geo.lat, geo.lon);
    } catch {
      /* keep default location if geocoding fails */
    }
  }

  async function verifyOtp() {
    if (otp !== DEMO_OTP) {
      setError("Incorrect OTP. Hint: 1234");
      return;
    }
    setError("");
    setBusy(true);
    try {
      // If the farmer already exists, log straight in.
      const farmer = await api.getFarmer(phone);
      await applyLocation(farmer.district, farmer.state);
      setFarmer(farmer);
    } catch {
      // New farmer -> collect profile.
      setStep("profile");
    } finally {
      setBusy(false);
    }
  }

  async function saveProfile() {
    if (!name.trim()) {
      setError("Please enter your name");
      return;
    }
    setBusy(true);
    setError("");
    try {
      const farmer = await api.registerFarmer({
        phone,
        name,
        village,
        district,
        state,
        language: lang,
      });
      await applyLocation(district, state);
      setFarmer(farmer);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="flex h-full w-full items-center justify-center p-0 sm:p-6">
      <div className="flex h-full w-full max-w-[420px] flex-col justify-center bg-gradient-to-b from-brand-green to-brand-greenDark px-7 py-10 text-white shadow-2xl sm:h-[860px] sm:rounded-[2.5rem]">
        <div className="mb-8 text-center">
          <div className="text-6xl">🚜</div>
          <h1 className="mt-3 text-3xl font-extrabold">{tr("appName", lang)}</h1>
          <p className="mt-1 text-green-100">{tr("tagline", lang)}</p>
        </div>

        <div className="rounded-2xl bg-white p-5 text-slate-800">
          {error && (
            <div className="mb-3">
              <Banner tone="error">{error}</Banner>
            </div>
          )}

          {step === "phone" && (
            <div className="space-y-4">
              <Input
                label={tr("phone", lang)}
                inputMode="numeric"
                maxLength={10}
                value={phone}
                onChange={(e) => setPhone(e.target.value.replace(/\D/g, ""))}
                placeholder="9876543210"
              />
              <Button
                onClick={() => phone.length >= 10 && setStep("otp")}
                disabled={phone.length < 10}
              >
                {tr("sendOtp", lang)}
              </Button>
            </div>
          )}

          {step === "otp" && (
            <div className="space-y-4">
              <Input
                label={tr("enterOtp", lang)}
                inputMode="numeric"
                maxLength={4}
                value={otp}
                onChange={(e) => setOtp(e.target.value.replace(/\D/g, ""))}
                placeholder="1234"
              />
              <p className="text-xs text-slate-400">{tr("otpHint", lang)}</p>
              <Button onClick={verifyOtp} disabled={busy}>
                {tr("verify", lang)}
              </Button>
            </div>
          )}

          {step === "profile" && (
            <div className="space-y-3">
              <Input label={tr("name", lang)} value={name} onChange={(e) => setName(e.target.value)} />
              <Input label={tr("village", lang)} value={village} onChange={(e) => setVillage(e.target.value)} />
              <Select
                label={tr("state", lang)}
                options={STATE_LIST}
                value={state}
                placeholder={tr("selectState", lang)}
                onChange={(e) => {
                  setState(e.target.value);
                  setDistrict("");
                }}
              />
              <Select
                label={tr("district", lang)}
                options={state ? STATES_DISTRICTS[state] || [] : []}
                value={district}
                disabled={!state}
                placeholder={tr("selectDistrict", lang)}
                onChange={(e) => setDistrict(e.target.value)}
              />
              <Button onClick={saveProfile} disabled={busy}>
                {tr("save", lang)}
              </Button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
