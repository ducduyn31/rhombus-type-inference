import React from "react";
import {Card, FileUploader, Label} from "@repo/ui/components";

export default function Page(): React.ReactElement {
  return (
    <main className="flex flex-col items-center justify-between min-h-screen p-24">
      <Card className="w-full p-24 flex flex-col gap-y-5">
        <Label type="header">Upload file</Label>
        <FileUploader size="large" />
        <div className="flex justify-between text-slate-400">
          <Label>Supported formats: XLS, XLSX, CSV</Label>
          <Label>Maximum size: 2GB</Label>
        </div>
      </Card>
    </main>
  );
}
