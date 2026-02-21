import { useEffect, useRef, useState, useImperativeHandle, forwardRef } from 'react';

const CameraFeed = forwardRef(function CameraFeed({ onStreamReady }, ref) {
  const videoRef = useRef(null);
  const streamRef = useRef(null);
  const canvasRef = useRef(document.createElement('canvas'));
  const [error, setError] = useState(null);

  async function startCamera() {
    setError(null);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: 640, height: 480, facingMode: 'user' },
        audio: false,
      });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
      }
      onStreamReady?.();
    } catch (err) {
      if (err.name === 'NotAllowedError') {
        setError('Camera permission denied. Please allow camera access and retry.');
      } else {
        setError('Could not access camera: ' + err.message);
      }
    }
  }

  useEffect(() => {
    startCamera();
    return () => {
      streamRef.current?.getTracks().forEach(t => t.stop());
    };
  }, []);

  // Expose captureFrame() to parent via ref
  useImperativeHandle(ref, () => ({
    captureFrame() {
      const video = videoRef.current;
      if (!video || video.readyState < 2) return null;
      const canvas = canvasRef.current;
      canvas.width = video.videoWidth || 640;
      canvas.height = video.videoHeight || 480;
      canvas.getContext('2d').drawImage(video, 0, 0);
      return canvas.toDataURL('image/jpeg', 0.7);
    },
    getVideoElement() {
      return videoRef.current;
    },
  }));

  if (error) {
    return (
      <div className="camera-error">
        <p>{error}</p>
        <button className="btn btn-secondary" onClick={startCamera}>Retry</button>
      </div>
    );
  }

  return (
    <video
      ref={videoRef}
      className="camera-video"
      autoPlay
      playsInline
      muted
    />
  );
});

export default CameraFeed;
