"use client"

import type {HTMLAttributes} from "react";
import * as React from "react";
import {forwardRef, useRef} from "react";
import type {ClassValue} from "clsx";
import {cn} from "@repo/ui/utils";
import {FileUploaderProvider, useFileUploader} from "@ui/components/complex/file-uploader/context.tsx";
import {convertBytesToReadable} from "@ui/components/complex/utils/strings.ts";
import {UploadIcon} from "../../icons/upload-icon";
import {Label} from "../../ui/label.tsx";

interface FileUploaderProps extends HTMLAttributes<HTMLInputElement> {
  size: 'small' | 'medium' | 'large';
  accept?: string;
  supportedFormats?: string;
  maxFileSize?: number;
}

const FileUploader = forwardRef<
  HTMLInputElement,
  FileUploaderProps
>(({size, maxFileSize, supportedFormats, ...rest}, forwardedRef) => {

  const localRef = useRef<HTMLInputElement | null>(null);

  const assignRef = (inp: HTMLInputElement | null): void => {
    localRef.current = inp;
    if (forwardedRef) {
      if (typeof forwardedRef === "function") {
        forwardedRef(inp);
      } else {
        forwardedRef.current = inp;
      }
    }
  };

  return (
    <FileUploaderProvider inputRef={localRef}>
      <input {...rest} className="ui-hidden" hidden ref={assignRef} type="file"/>
      <FileDropZone size={size} title={rest.title}/>
      {
        size === "large" && (
          <div className="flex justify-between text-slate-400">
            {supportedFormats ? <Label>Supported formats: {supportedFormats}</Label> : null}
            {maxFileSize ? <Label>Maximum size: {convertBytesToReadable(maxFileSize)}</Label> : null}
          </div>
        )
      }
    </FileUploaderProvider>);
});

const FileDropZone = React.forwardRef<
  HTMLDivElement,
  HTMLAttributes<HTMLDivElement> & { size: 'small' | 'medium' | 'large' }
>((props, ref) => {
  const {triggerFileSelect} = useFileUploader();

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
      props.className
    )}>
      {props.size === "large" && <UploadIcon className="ui-h-16 ui-w-16"/>}
      <span>
        <Label className="ui-text-xl">Drag and Drop file here or </Label>
        <Label className="ui-text-xl ui-font-bold ui-underline" onClick={triggerFileSelect}
               type="link">Choose file</Label>
      </span>
    </div>
  );
});

FileUploader.displayName = "FileUploader";
FileDropZone.displayName = "FileDropZone";


export {FileUploader};
