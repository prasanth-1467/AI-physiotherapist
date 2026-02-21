import { useEffect, useRef } from 'react';

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws/exercise';
const MAX_RETRIES = 3;
const FRAME_INTERVAL_MS = 1000 / 30; // 30fps

export default function WebSocketManager({
  captureFrame,
  onKeypointsReceived,
  onAngleReceived,
  onVoiceCueReceived,
  active = true,
}) {
  const wsRef = useRef(null);
  const retriesRef = useRef(0);
  const intervalRef = useRef(null);
  const activeRef = useRef(active);

  useEffect(() => { activeRef.current = active; }, [active]);

  function connect() {
    if (wsRef.current) {
      wsRef.current.onclose = null;
      wsRef.current.close();
    }

    const ws = new WebSocket(WS_URL);
    wsRef.current = ws;

    ws.onopen = () => {
      retriesRef.current = 0;
      // Start sending frames
      intervalRef.current = setInterval(() => {
        if (!activeRef.current) return;
        if (ws.readyState !== WebSocket.OPEN) return;
        const frame = captureFrame?.();
        if (frame) ws.send(JSON.stringify({ type: 'frame', data: frame }));
      }, FRAME_INTERVAL_MS);
    };

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);
        if (msg.type === 'keypoints') onKeypointsReceived?.(msg.data);
        else if (msg.type === 'angles') onAngleReceived?.(msg.data);
        else if (msg.type === 'voice_cue') onVoiceCueReceived?.(msg.text);
      } catch (_) {}
    };

    ws.onerror = () => {};

    ws.onclose = () => {
      clearInterval(intervalRef.current);
      if (retriesRef.current < MAX_RETRIES && activeRef.current) {
        const delay = Math.pow(2, retriesRef.current) * 1000;
        retriesRef.current += 1;
        setTimeout(connect, delay);
      }
    };
  }

  useEffect(() => {
    if (!active) {
      clearInterval(intervalRef.current);
      wsRef.current?.close();
      return;
    }
    connect();
    return () => {
      clearInterval(intervalRef.current);
      if (wsRef.current) {
        wsRef.current.onclose = null;
        wsRef.current.close();
      }
    };
  }, [active]);

  return null;
}
