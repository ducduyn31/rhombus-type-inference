import type {FC} from "react";
import {lazy} from "react";
import {CheckCircledIcon, TrashIcon} from "@radix-ui/react-icons";
import {Card} from "../../ui/card";
import {Progress} from "../../ui/progress";

const ExcelIcon = lazy(() => import("../../icons/excel-icon")
  .then((module) => ({default: module.ExcelIcon})));
const CsvIcon = lazy(() => import("../../icons/csv-icon")
  .then((module) => ({default: module.CsvIcon})));

interface FilePreviewProps {
  file?: File;
  uploadProgress?: number;
  state?: "uploaded" | "uploading" | "none";
  onRemove?: () => void;
}

const FilePreview: FC<FilePreviewProps> = ({
                                             file,
                                             uploadProgress,
                                             state = "none",
                                             onRemove
                                           }) => {
  const fileType = file?.type;
  const isExcel = fileType === "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" ||
    fileType === "application/vnd.ms-excel";

  const convertBytesToReadable = (bytes: number): string => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB", "TB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`;
  }

  const title = (): string => {
    if (state === "none") {
      return file?.name || "Your file";
    }
    if (state === "uploading") {
      return "Uploading";
    }
    return "Upload Completed";
  }

  return (
    <Card className="ui-p-5 ui-flex ui-gap-x-3">
      <div className="ui-flex ui-items-center">
        {isExcel ? <ExcelIcon className="ui-w-12 ui-h-12 ui-mx-auto"/> :
          <CsvIcon className="ui-w-12 ui-h-12 ui-mx-auto"/>}
      </div>
      <div className="ui-flex-grow">
        <p className="ui-font-semibold ui-text-xl">{title()}</p>
        {state === "none" &&
            <p className="ui-font-light ui-accent-gray-500 ui-text-sm">Size: {convertBytesToReadable(file?.size || 0)}</p>}
        {state === "uploading" && (
          <div className="ui-flex ui-gap-x-5 ui-items-center">
            <p
              className="ui-font-light ui-accent-gray-500 ui-text-sm">{file?.name}</p>
            <p
              className="ui-font-light ui-accent-gray-500 ui-text-sm ui-flex-grow">Size: {convertBytesToReadable(file?.size || 0)}</p>
            <p className="ui-font-semibold ui-text-sm ui-accent-gray-500">{uploadProgress}%</p>
          </div>
        )}
        {
          state === "uploaded" && (
            <div className="ui-flex ui-gap-x-5 ui-items-center">
              <span className="ui-flex ui-gap-2 ui-items-center">
                <CheckCircledIcon className="ui-w-6 ui-h-6 ui-text-green-500 ui-align-text-bottom"/>
                <p
                  className="ui-font-light ui-accent-gray-500 ui-text-sm">{file?.name}</p>
              </span>
              <p
                className="ui-font-light ui-accent-gray-500 ui-text-sm">Size: {convertBytesToReadable(file?.size || 0)}</p>
            </div>
          )
        }
        {state === "uploading" ? <Progress className="ui-mt-2" value={uploadProgress}/> : <div className="ui-mt-4"/>}
      </div>
      <button className="ui-ml-auto" onClick={onRemove} type="button">
        <TrashIcon className="ui-w-6 ui-h-6"/>
      </button>
    </Card>
  );
}

export {FilePreview};