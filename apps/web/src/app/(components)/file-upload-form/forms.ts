import type {ZodType} from "zod";
import {z} from "zod";

const MAX_FILE_SIZE = 1024 * 1024 * 1024 * 2; // 2GB

const ACCEPTED_FILE_TYPES = [
  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  "application/vnd.ms-excel",
  "text/csv",
];

const FormSchema: ZodType = z.object({
  file: z.instanceof(File).refine((file) =>
      file.size <= MAX_FILE_SIZE,
    "Maximum file size is 2GB",
  ).refine((file) =>
      ACCEPTED_FILE_TYPES.includes(file.type),
    "Supported formats are XLS, XLSX, CSV",
  ),
});

interface FormType {
  file?: File;
}

export {FormSchema};
export type {FormType};
