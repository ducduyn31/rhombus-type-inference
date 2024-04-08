import {produce} from "immer";
import axios from "axios";
import type {GetState, InferState, Response, ResponseDataGeneric, SessionState, SetState} from "../types.ts";
import {convertNpTypeToHumanReadable} from "../mapper.ts";


export const setupSSEReceiver = (set: SetState, get: GetState): boolean => {
  const currentSSE = get().sse;
  const currentSessionId = get().sessionId;
  if (currentSSE) {
    currentSSE.close();
  }
  if (!currentSessionId) {
    return false;
  }
  set(produce((draft: InferState) => {
    draft.sse = new EventSource(`/sse/events/${draft.sessionId}/`);
    draft.sse.onmessage = onSSEMessage.bind(null, set, get);
    draft.sse.onerror = () => {
      draft.sse?.close();
    }
  }));
  return true;
}

const onSSEMessage = (set: SetState, get: GetState, e: MessageEvent): void => {
  const message = JSON.parse(e.data as string) as { sessionId: string, state: string };
  if (message.state === "success") {
    get().sse?.close();
    void updateDtypes(set, get);
  } else if (message.state === "error") {
    get().sse?.close();
  }
  set(produce((draft: InferState) => {
    draft.currentState = message.state as SessionState;
  }));
}

const updateDtypes = async (set: SetState, get: GetState): Promise<void> => {
  const sessionId = get().sessionId;
  if (!sessionId) {
    return;
  }
  const response = await axios.get<Response>(`/api/sessions/${sessionId}/`);
  if (!response.data.data) return;
  const data = response.data.data as ResponseDataGeneric;
  const dtypes = data.columns_dtypes;
  if (!dtypes) return;
  set(produce((draft: InferState) => {
    draft.result = convertNpTypeToHumanReadable(dtypes);
  }));
}