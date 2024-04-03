// tailwind config is required for editor support

import type { Config } from "tailwindcss";
import sharedConfig from "@repo/tailwind-config";

const config: Pick<Config, "content" | "presets" | "prefix"> = {
  content: ["./src/app/**/*.tsx"],
  presets: [sharedConfig],
  prefix: "ui-",
};

export default config;
