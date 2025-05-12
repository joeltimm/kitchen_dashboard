import { useState, useEffect, useRef } from "react";
import { Rnd } from "react-rnd";

export default function OneDrivePhotoWidget({ profile = "default" }) {
  const [imageUrl, setImageUrl] = useState(null);
  const [intervalMs, setIntervalMs] = useState(60000);
  const [dimensions, setDimensions] = useState({ width: 400, height: 300 });
  const [error, setError] = useState(null);

  const fetchImage = async () => {
    try {
      const res = await fetch("/api/onedrive-image");
      const data = await res.json();
      if (data.image_url) setImageUrl(data.image_url);
    } catch {
      setError("Image load failed.");
    }
  };

  const fetchSettings = async () => {
    const res = await fetch(`/api/photo-widget-settings?profile=${profile}`);
    if (res.ok) {
      const data = await res.json();
      if (data.intervalMs) setIntervalMs(data.intervalMs);
      if (data.width && data.height) setDimensions({ width: data.width, height: data.height });
    }
  };

  const saveSettings = async () => {
    await fetch("/api/photo-widget-settings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        profile,
        intervalMs,
        ...dimensions,
      }),
    });
  };

  useEffect(() => {
    fetchSettings();
  }, [profile]);

  useEffect(() => {
    fetchImage();
    const id = setInterval(fetchImage, intervalMs);
    return () => clearInterval(id);
  }, [intervalMs]);

  return (
    <div className="my-4">
      <Rnd
        size={dimensions}
        onResizeStop={(e, direction, ref) =>
          setDimensions({ width: parseInt(ref.style.width), height: parseInt(ref.style.height) })
        }
        bounds="window"
        className="border shadow rounded-xl p-2 bg-white"
      >
        <div className="flex flex-col h-full">
          <div className="font-bold mb-2">📷 OneDrive Photo - {profile}</div>
          {imageUrl ? (
            <img
              src={imageUrl}
              alt="OneDrive"
              className="flex-1 object-cover rounded"
              style={{ width: "100%", height: "100%" }}
            />
          ) : (
            <p className="text-gray-500">{error || "Loading..."}</p>
          )}
        </div>
      </Rnd>

      <div className="mt-3 space-y-2">
        <label className="block text-sm">Refresh Interval (seconds)</label>
        <input
          type="number"
          min="5"
          value={intervalMs / 1000}
          onChange={(e) => setIntervalMs(Number(e.target.value) * 1000)}
          className="border px-2 py-1 rounded w-32"
        />
        <button
          onClick={saveSettings}
          className="ml-4 px-4 py-1 bg-blue-600 text-white rounded"
        >
          Save Settings
        </button>
      </div>
    </div>
  );
}
