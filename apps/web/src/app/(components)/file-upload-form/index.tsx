"use client"
import {Alert, AlertDescription, AlertTitle, Button, FilePreview, FileUploader, Label} from "@repo/ui/components";
import type {FC} from "react";
import React, {useCallback, useEffect} from "react";
import {Controller, FormProvider, useForm, useFormContext} from "react-hook-form";
import {zodResolver} from "@hookform/resolvers/zod";
import {toast} from "sonner";
import {useInference} from "../../(api)/inference-context";
import type {FormType} from "./forms";
import {FormSchema} from "./forms";

type Optional<T> = T | null | undefined;

export const UploadForm: FC = () => {

  const inferFile = useInference((state) => state.inferFile);
  const currentState = useInference((state) => state.currentState);
  const resetState = useInference((state) => state.reset);
  const error = useInference((state) => state.error);

  const methods = useForm<FormType>({
    resolver: zodResolver(FormSchema),
  });

  const selectedFile = methods.watch("file") as Optional<File>;

  const resetForm = useCallback((): void => {
    methods.setValue("file", undefined);
    void methods.trigger("file");
    resetState();
  }, [methods, resetState])

  useEffect(() => {
    if (currentState === "error") {
      toast.error("An error occurred while processing the file");
    } else if (currentState === "success") {
      toast.success("Successfully processed the file");
    }
  }, [currentState])

  if (currentState === "success") {
    return null;
  }

  const shouldAllowSubmit = methods.formState.isValid && ["init", "idle", "error"].includes(currentState);
  const buttonLabel = (() => {
    switch (currentState) {
      case "init":
        return "Submit";
      case "generate_presigned_url":
        return "Uploading...";
      case "file_uploaded":
        return "File uploaded. Processing...";
      case "validate_file":
        return "Validating...";
      case "infer_file":
        return "Processing...";
      case "error":
        return "Error. Try again";
      default:
        return "Submit";
    }
  })()

  const handleSubmit = async (data: FormType): Promise<void> => {
    if (!data.file) return;
    await inferFile(data.file)
  }

  return (
    <FormProvider {...methods}>
      {error ? (
        <Alert className="mb-5" variant="destructive">
          <AlertTitle>{error.message}</AlertTitle>
          <AlertDescription>{error.description}</AlertDescription>
        </Alert>
      ) : null}
      <form className="flex flex-col gap-y-5" onSubmit={methods.handleSubmit(handleSubmit)}>
        <SelectFileForm/>
        {selectedFile ? <FilePreview file={selectedFile} onRemove={resetForm}/> : null}
        {methods.formState.isValid ? <div className="flex justify-end">
          <Button className="max-w-64 min-w-40" disabled={!shouldAllowSubmit} type="submit">{buttonLabel}</Button>
        </div> : null}
      </form>
    </FormProvider>
  )
}

const SelectFileForm: FC = () => {

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