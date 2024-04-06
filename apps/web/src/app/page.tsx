import React from "react";
import {UploadForm} from "./(components)/file-upload-form";

export default function Page(): React.ReactElement {
  return (
    <main className="flex flex-col items-center justify-between min-h-screen p-24">
      <UploadForm/>
    </main>
  );
}
