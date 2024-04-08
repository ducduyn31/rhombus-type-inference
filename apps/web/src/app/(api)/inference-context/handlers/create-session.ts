import {produce} from "immer";
import axios from "axios";
import {toast} from "sonner";
import type {InferState, Response, SetState} from "../types.ts";

export const createSession = async (set: SetState): Promise<boolean> => {
  set(produce((draft: InferState) => {
    draft.loading = true;
  }));
  try {
    const response = await axios.post<Response>("/api/sessions/");
    if (response.data.data) {
      const sessionId = response.data.data.session_id;
      set(produce((draft: InferState) => {
        draft.sessionId = sessionId;
      }));
    }
    return true;
  } catch (e) {
    toast.error("Failed to create session");
    return false;
  } finally {
    set(produce((draft: InferState) => {
      draft.loading = false;
    }));
  }
}