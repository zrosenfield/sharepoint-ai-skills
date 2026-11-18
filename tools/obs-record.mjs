/**
 * OBS WebSocket recording helper for --record mode.
 *
 * Requires OBS 28+ with the built-in WebSocket server enabled:
 *   OBS → Tools → WebSocket Server Settings → Enable WebSocket Server
 *   Default port: 4455. Password is optional.
 *
 * Set obsPassword in demo.config.json (or OBS_PASSWORD env var).
 */

import { OBSWebSocket } from 'obs-websocket-js';

/**
 * Attempt to connect to OBS WebSocket. Returns null if OBS is not reachable.
 */
export async function tryConnectOBS(url = 'ws://127.0.0.1:4455', password = '') {
  const obs = new OBSWebSocket();
  try {
    await obs.connect(url, password || undefined, { rpcVersion: 1 });
    return obs;
  } catch {
    return null;
  }
}

/**
 * Check whether OBS is downscaling the output resolution and fix it if so.
 * Returns a summary string for logging.
 */
export async function ensureFullResolution(obs) {
  try {
    const s = await obs.call('GetVideoSettings');
    const { baseWidth, baseHeight, outputWidth, outputHeight, fpsNumerator, fpsDenominator } = s;
    const fps = (fpsNumerator / fpsDenominator).toFixed(0);
    if (outputWidth !== baseWidth || outputHeight !== baseHeight) {
      await obs.call('SetVideoSettings', {
        fpsNumerator,
        fpsDenominator,
        baseWidth,
        baseHeight,
        outputWidth: baseWidth,
        outputHeight: baseHeight,
      });
      return `${outputWidth}×${outputHeight} → fixed to ${baseWidth}×${baseHeight} @ ${fps}fps`;
    }
    return `${outputWidth}×${outputHeight} @ ${fps}fps`;
  } catch {
    return null;
  }
}

/**
 * Start OBS recording. Returns the wall-clock ms timestamp when recording
 * started, so callers can compute videoOffsetMs for Remotion sync.
 */
export async function startRecording(obs) {
  await obs.call('StartRecord');
  return Date.now();
}

/**
 * Stop OBS recording. Waits for the STOPPED state (not just STOPPING) which
 * is when OBS emits the output file path.
 */
export async function stopRecording(obs) {
  // Use on() not once() — OBS fires STOPPING first, then STOPPED (with the path).
  const pathPromise = new Promise((resolve) => {
    const timeout = setTimeout(() => resolve(null), 10000);
    const handler = (data) => {
      if (data.outputState === 'OBS_WEBSOCKET_OUTPUT_STOPPED') {
        clearTimeout(timeout);
        obs.off('RecordStateChanged', handler);
        resolve(data.outputPath ?? null);
      }
    };
    obs.on('RecordStateChanged', handler);
  });
  await obs.call('StopRecord');
  return pathPromise;
}

/**
 * Switch OBS to the named program scene. No-ops silently if the scene
 * doesn't exist (OBS will throw; we catch and warn).
 */
export async function switchScene(obs, sceneName) {
  await obs.call('SetCurrentProgramScene', { sceneName });
}

export function disconnectOBS(obs) {
  try { obs.disconnect(); } catch { /* ignore */ }
}
