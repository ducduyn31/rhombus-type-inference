"use client"
import {Button, Card, FileUploader, Label} from "@ui/components";
import type {FC} from "react";
import React from "react";
import {FormProvider, useForm} from "react-hook-form";

const UploadForm: FC = () => {

  const methods = useForm();

  return (
    <FormProvider {...methods}>
      <Card className="w-full p-24 flex flex-col gap-y-5">
        <Label type="header">Upload file</Label>
        <FileUploader
          accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"
          size="large"/>
        <div className="flex justify-between text-slate-400">
          <Label>Supported formats: XLS, XLSX, CSV</Label>
          <Label>Maximum size: 2GB</Label>
        </div>
        <Button>Upload</Button>
      </Card>
    </FormProvider>
  )
}

export {UploadForm}