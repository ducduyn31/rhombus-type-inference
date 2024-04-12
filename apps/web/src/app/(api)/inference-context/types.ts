import type {StoreApi} from "zustand";

type SessionState =
  "idle"
  | "init"
  | "generate_presigned_url"
  | "file_uploaded"
  | "validate_file"
  | "infer_file"
  | "success"
  | "error";

interface ResponseError {
  code: number;
  description: string | null;
  message: string;
  mime_type?: string;
}

interface ResponseDataPresignUrlGenerate {
  upload_url: string;
  session_id: string;
  state: "generate_presigned_url";
}

interface ResponseDataGeneric {
  filename?: string;
  mime_type?: string;
  session_id: string;
  columns_dtypes?: Record<string, string>;
  state: Omit<SessionState, "generate_presigned_url">
}

interface Response {
  message: string;
  error?: ResponseError;
  data?: ResponseDataPresignUrlGenerate | ResponseDataGeneric;
}

interface InferState {
  currentState: SessionState;
  loading: boolean;
  sessionId: string | null;
  uploadUrl: string | null;
  error: ResponseError | null;
  sse: EventSource | null;
  result: Record<string, string> | null;
  inferFile: (file: File) => Promise<void>;
  reset: () => void;
}

type SetState = StoreApi<InferState>["setState"];
type GetState = StoreApi<InferState>["getState"];

export type {
  SessionState,
  ResponseError,
  ResponseDataPresignUrlGenerate,
  ResponseDataGeneric,
  Response,
  InferState,
  GetState,
  SetState
};