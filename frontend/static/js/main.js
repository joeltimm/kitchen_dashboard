import { createRoot } from "react-dom/client";
import Clock from "./widgets/Clock";
import Weather from "./widgets/Weather";
import Calendar from "./widgets/Calendar";
import Photo from "./widgets/Photo";
import WidgetContainer from "./widgets/WidgetContainer";
import ProfileManager from "./components/ProfileManager";
import { useState, useEffect } from "react";

function App() {
  const [profileName, setProfileName] = useState("default");
  const [widgetSettings, setWidgetSettings] = useState({});

  useEffect(() => {
    fetch(`/api/widgets/settings?profile=${profileName}`)
      .then(res => res.json())
      .then(data => setWidgetSettings(data));
  }, [profileName]);

  const handleUpdate = (id, settings) => {
    setWidgetSettings(prev => ({
      ...prev,
      [id]: settings
    }));
  };

  const saveProfile = () => {
    fetch("/api/widgets/settings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ profile: profileName, settings: widgetSettings })
    });
  };

  return (
    <div>
      <ProfileManager
        profileName={profileName}
        onChange={setProfileName}
        onSave={saveProfile}
      />

      {Object.entries(widgetSettings).map(([id, settings]) => {
        const Widget = { clock: Clock, weather: Weather, calendar: Calendar, photo: Photo }[id];
        return (
          <WidgetContainer key={id} id={id} settings={settings} onUpdate={handleUpdate}>
            <Widget />
          </WidgetContainer>
        );
      })}
    </div>
  );
}

const root = createRoot(document.getElementById("root"));
root.render(<App />);
