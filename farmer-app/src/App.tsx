import { useState } from "react";
import { useApp } from "./store";
import { Shell, type Tab } from "./components/Shell";
import { Auth } from "./screens/Auth";
import { Home } from "./screens/Home";
import { Market } from "./screens/Market";
import { Advisory } from "./screens/Advisory";
import { Pest } from "./screens/Pest";
import { Profile } from "./screens/Profile";

export default function App() {
  const { farmer } = useApp();
  const [tab, setTab] = useState<Tab>("home");

  if (!farmer) return <Auth />;

  return (
    <Shell tab={tab} setTab={setTab}>
      {tab === "home" && <Home />}
      {tab === "market" && <Market />}
      {tab === "advisory" && <Advisory />}
      {tab === "pest" && <Pest />}
      {tab === "profile" && <Profile />}
    </Shell>
  );
}
