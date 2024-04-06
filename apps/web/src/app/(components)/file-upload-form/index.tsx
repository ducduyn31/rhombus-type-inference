"use client"
import {Button, Card, FilePreview, FileUploader, Label} from "@ui/components";
import type {ReactElement, ReactNode} from "react";
import React from "react";
import {Controller, FormProvider, useForm, useFormContext} from "react-hook-form";
import {zodResolver} from "@hookform/resolvers/zod";
import type {FormType} from "./forms";
import {FormSchema} from "./forms";

type Optional<T> = T | null | undefined;

function UploadForm(): ReactElement {

  const methods = useForm<FormType>({
    resolver: zodResolver(FormSchema),
  });

  const selectedFile = methods.watch("file") as Optional<File>;

  const resetForm = (): void => {
    methods.setValue("file", undefined);
    void methods.trigger("file");
  }

  return (
    <FormProvider {...methods}>
      <Card className="w-full p-24">
        <form className="flex flex-col gap-y-5">
          <SelectFileForm/>
          {selectedFile ? <FilePreview file={selectedFile} onRemove={resetForm}/> : null}
          {methods.formState.isValid ? <div className="flex justify-end">
              <Button className="max-w-64 min-w-40" type="submit">Upload</Button>
            </div> : null}
        </form>
      </Card>
    </FormProvider>
  )
}

function SelectFileForm(): ReactNode {

  const methods = useFormContext<FormType>();

  if (methods.watch("file")) {
    return null;
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>): void => {
    const file = e.target.files?.[0];
    if (file) {
      methods.setValue("file", file);
      void methods.trigger("file");
    }
  }

  return (
    <>
      <Label type="header">Upload file</Label>
      <Controller name="file" render={({field}) => (
        <FileUploader
          {...field}
          accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"
          maxFileSize={1024 * 1024 * 1024 * 2}
          onChange={handleFileChange}
          size="large"
          supportedFormats="XLS, XLSX, CSV"/>
      )}/>
    </>
  )
}

export {UploadForm}