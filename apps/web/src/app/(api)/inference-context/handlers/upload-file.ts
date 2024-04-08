import {produce} from "immer";
import {toast} from "sonner";
import axios from "axios";
import type {GetState, InferState, SetState} from "../types.ts";


export const uploadFile = async (set: SetState, get: GetState, file: File): Promise<boolean> => {
  set(produce((draft: InferState) => {
    draft.loading = true;
  }));
  try {
    const sessionId = get().sessionId;
    const uploadUrl = get().uploadUrl;
    if (!sessionId || !uploadUrl) {
      toast.error("Session ID or upload URL is missing");
      return false;
    }
    const response = await axios.put(`/storage${uploadUrl}`, file, {
      headers: {
        "Content-Type": file.type,
      },
    });
    return response.status === 200;
  } catch (e) {
    toast.error("Failed to upload file");
    return false;
  } finally {
    set(produce((draft: InferState) => {
      draft.loading = false;
    }));
  }
}