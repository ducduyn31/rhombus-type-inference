import type {HTMLAttributes} from "react";
import * as React from "react";
import type {ClassValue} from "clsx";
import {cn} from "@repo/ui/utils";
import {UploadIcon} from "../../icons/upload-icon";
import {Label} from "../../ui/label.tsx";

interface FileUploaderProps extends HTMLAttributes<HTMLInputElement> {
  size: 'small' | 'medium' | 'large';
  onFileChange?: (file: File) => void;
}

const FileUploader = React.forwardRef<
  HTMLInputElement,
  FileUploaderProps
>(({size, ...rest}, ref) => {

  return (
    <>
      <input ref={ref} type="file" {...rest} className="ui-hidden" hidden/>
      <FileDropZone size={size} title={rest.title}/>
    </>);
});

const FileDropZone = React.forwardRef<
  HTMLDivElement,
  HTMLAttributes<HTMLDivElement> & { size: 'small' | 'medium' | 'large' }
>((props, ref) => {
  const sizeToClass: Record<string, ClassValue> = {
    small: "",
    medium: "ui-h-32",
    large: "ui-h-64",
  } as const;

  return (
    <div ref={ref} {...props} className={cn(
      props.size !== "small" && "ui-border-2 ui-border-dashed ui-border-gray-300 ui-rounded-l",
      "ui-flex ui-flex-col ui-justify-center ui-items-center ui-gap-y-5",
      "ui-transition ui-duration-150 ui-ease-in-out",
      "ui-bg-secondary",
      sizeToClass[props.size],
      // "ui-flex ui-justify-center ui-items-center ui-text-gray-400 ui-text-sm",
      // "ui-font-medium ui-bg-gray-50 ui-transition ui-duration-150 ui-ease-in-out",
      props.className
    )}>
      {props.size === "large" && <UploadIcon className="ui-h-16 ui-w-16"/>}
      <span>
        <Label className="ui-text-xl">Drag and Drop file here or </Label>
        <Label className="ui-text-xl ui-font-bold ui-underline" type="link">Choose file</Label>
      </span>
    </div>
  );
});

FileUploader.displayName = "FileUploader";
FileDropZone.displayName = "FileDropZone";


export {FileUploader};
