import {createStore} from 'zustand';
import type {InferState, SessionState} from "./types.ts";
import {createSession, generatePresignedUrl, setupSSEReceiver, uploadFile} from "./handlers";

export const inferStore = createStore<InferState>((set, get) => ({
  currentState: "idle" as SessionState,
  loading: false,
  sessionId: null,
  uploadUrl: null,
  result: null,
  sse: null,
  inferFile: async (file: File) => {
    // Create Session
    if (!await createSession(set)) return;
    // Setup SSE Receiver
    if (!setupSSEReceiver(set, get)) return;
    // Generate Presigned URL
    if (!await generatePresignedUrl(set, get)) return;
    // Upload file
    await uploadFile(set, get, file);
  },
  reset: () => {
    get().sse?.close();
    set({currentState: "idle", loading: false, sessionId: null, uploadUrl: null, result: null, sse: null});
  }
}));
