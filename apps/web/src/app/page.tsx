import type {FC} from "react";
import React from "react";
import {Card, Toaster} from "@repo/ui/components";
import {UploadForm} from "./(components)/file-upload-form";
import {TypeDisplay} from "./(components)/type-displayer";
import {InferenceContextProvider} from "./(api)/inference-context";

const Page: FC = () => {
  return (
    <main className="flex flex-col items-center justify-between min-h-screen p-24">
      <InferenceContextProvider>
        <Card className="w-full p-24">
          <UploadForm/>
          <TypeDisplay/>
        </Card>
      </InferenceContextProvider>
      <Toaster/>
    </main>
  );
}

export default Page;