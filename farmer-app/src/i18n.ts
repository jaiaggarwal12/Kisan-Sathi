// Lightweight multilingual support: English, Hindi, Punjabi.
export type Lang = "en" | "hi" | "pa";

type Dict = Record<string, { en: string; hi: string; pa: string }>;

export const T: Dict = {
  appName: { en: "Kisan Sathi", hi: "किसान साथी", pa: "ਕਿਸਾਨ ਸਾਥੀ" },
  tagline: {
    en: "Your smart farming companion",
    hi: "आपका स्मार्ट खेती साथी",
    pa: "ਤੁਹਾਡਾ ਸਮਾਰਟ ਖੇਤੀ ਸਾਥੀ",
  },
  phone: { en: "Mobile number", hi: "मोबाइल नंबर", pa: "ਮੋਬਾਈਲ ਨੰਬਰ" },
  sendOtp: { en: "Send OTP", hi: "OTP भेजें", pa: "OTP ਭੇਜੋ" },
  enterOtp: { en: "Enter OTP", hi: "OTP दर्ज करें", pa: "OTP ਦਰਜ ਕਰੋ" },
  verify: { en: "Verify & Continue", hi: "सत्यापित करें", pa: "ਤਸਦੀਕ ਕਰੋ" },
  otpHint: {
    en: "Demo OTP is 1234",
    hi: "डेमो OTP 1234 है",
    pa: "ਡੈਮੋ OTP 1234 ਹੈ",
  },
  home: { en: "Home", hi: "होम", pa: "ਹੋਮ" },
  market: { en: "Market", hi: "मंडी", pa: "ਮੰਡੀ" },
  advisory: { en: "Advisory", hi: "सलाह", pa: "ਸਲਾਹ" },
  pest: { en: "Pest", hi: "कीट", pa: "ਕੀਟ" },
  profile: { en: "Profile", hi: "प्रोफ़ाइल", pa: "ਪ੍ਰੋਫਾਈਲ" },
  weather: { en: "Weather", hi: "मौसम", pa: "ਮੌਸਮ" },
  cropHealth: { en: "Crop Health (NDVI)", hi: "फसल स्वास्थ्य (NDVI)", pa: "ਫਸਲ ਸਿਹਤ (NDVI)" },
  schemes: { en: "Government Schemes", hi: "सरकारी योजनाएँ", pa: "ਸਰਕਾਰੀ ਸਕੀਮਾਂ" },
  sos: { en: "SOS", hi: "आपातकाल", pa: "ਐਮਰਜੈਂਸੀ" },
  name: { en: "Full name", hi: "पूरा नाम", pa: "ਪੂਰਾ ਨਾਮ" },
  village: { en: "Village", hi: "गाँव", pa: "ਪਿੰਡ" },
  district: { en: "District", hi: "ज़िला", pa: "ਜ਼ਿਲ੍ਹਾ" },
  state: { en: "State", hi: "राज्य", pa: "ਰਾਜ" },
  save: { en: "Save & Continue", hi: "सहेजें", pa: "ਸੰਭਾਲੋ" },
  selectCommodity: { en: "Select commodity", hi: "फसल चुनें", pa: "ਫਸਲ ਚੁਣੋ" },
  selectState: { en: "Select state", hi: "राज्य चुनें", pa: "ਰਾਜ ਚੁਣੋ" },
  selectDistrict: { en: "Select district", hi: "ज़िला चुनें", pa: "ਜ਼ਿਲ੍ਹਾ ਚੁਣੋ" },
  selectMarket: { en: "Select market", hi: "मंडी चुनें", pa: "ਮੰਡੀ ਚੁਣੋ" },
  uploadPest: { en: "Upload pest photo", hi: "कीट फोटो अपलोड करें", pa: "ਕੀਟ ਫੋਟੋ ਅਪਲੋਡ ਕਰੋ" },
  detect: { en: "Detect", hi: "पहचानें", pa: "ਪਛਾਣੋ" },
  outbreaks: { en: "Nearby outbreaks", hi: "आस-पास के प्रकोप", pa: "ਨੇੜਲੇ ਪ੍ਰਕੋਪ" },
  logout: { en: "Logout", hi: "लॉग आउट", pa: "ਲੌਗ ਆਊਟ" },
  fertilizerAdvice: { en: "Fertilizer Advice", hi: "उर्वरक सलाह", pa: "ਖਾਦ ਸਲਾਹ" },
  whyThis: { en: "Why this advice?", hi: "यह सलाह क्यों?", pa: "ਇਹ ਸਲਾਹ ਕਿਉਂ?" },
  loading: { en: "Loading...", hi: "लोड हो रहा है...", pa: "ਲੋਡ ਹੋ ਰਿਹਾ ਹੈ..." },
};

export function tr(key: string, lang: Lang): string {
  const entry = T[key];
  if (!entry) return key;
  return entry[lang] || entry.en;
}
