import {produce} from "immer";
import {toast} from "sonner";
import axios from "axios";
import type {GetState, InferState, Response, ResponseDataPresignUrlGenerate, SetState} from "../types.ts";


export const generatePresignedUrl = async (set: SetState, get: GetState): Promise<boolean> => {
  set(produce((draft: InferState) => {
    draft.loading = true;
  }));
  try {
    const sessionId = get().sessionId;
    if (!sessionId) {
      toast.error("Session ID is missing");
      return false;
    }
    const response = await axios.put<Response>(`/api/sessions/${sessionId}/`, {
      state: "generate_presigned_url",
    });
    if (response.data.data && response.data.data.state === "generate_presigned_url") {
      const data = response.data.data as ResponseDataPresignUrlGenerate;
      set(produce((draft: InferState) => {
        draft.uploadUrl = data.upload_url;
      }));
      return true;
    }
    return false;
  } catch (e) {
    toast.error("Failed to generate presigned URL");
    return false;
  } finally {
    set(produce((draft: InferState) => {
      draft.loading = false;
    }));
  }
}