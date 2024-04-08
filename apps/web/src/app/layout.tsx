import "./globals.css";
import "@repo/ui/styles.css";
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import type {FC, PropsWithChildren} from "react";
import React from "react";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Rhombus AI - Type Inference",
  description: "Infer types from csv and excel files",
};

const RootLayout: FC<PropsWithChildren> = ({
  children,
}) => {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}

export default RootLayout;
