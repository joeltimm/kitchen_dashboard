import { Rnd } from "react-rnd";
import { useState } from "react";

export default function widget_container({ id, children, settings, onUpdate }) {
  const [enabled, setEnabled] = useState(settings.enabled);
  const [size, setSize] = useState({ width: settings.width, height: settings.height });

  if (!enabled) return null;

  return (
    <Rnd
      size={size}
      onResizeStop={(e, dir, ref, delta, pos) => {
        const newSize = { width: ref.offsetWidth, height: ref.offsetHeight };
        setSize(newSize);
        onUpdate(id, { ...settings, ...newSize });
      }}
    >
      <div className="widget-frame">
        <button onClick={() => { setEnabled(false); onUpdate(id, { ...settings, enabled: false }); }}>✖</button>
        {children}
      </div>
    </Rnd>
  );
}
