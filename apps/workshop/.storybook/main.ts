import type {StorybookConfig} from "@storybook/react-vite";
import tsconfigPaths from "vite-tsconfig-paths";

import {dirname, join} from "path";

/**
 * This function is used to resolve the absolute path of a package.
 * It is needed in projects that use Yarn PnP or are set up within a monorepo.
 */
function getAbsolutePath(value: string): any {
  return dirname(require.resolve(join(value, "package.json")));
}

const config: StorybookConfig = {
  stories: [
    "../stories/**/*.stories.@(js|jsx|mjs|ts|tsx)",
    "../../../packages/ui/src/components/**/*.stories.@(js|jsx|mjs|ts|tsx)",
  ],
  addons: [
    getAbsolutePath("@storybook/addon-onboarding"),
    getAbsolutePath("@storybook/addon-links"),
    getAbsolutePath("@storybook/addon-essentials"),
    getAbsolutePath("@chromatic-com/storybook"),
    getAbsolutePath("@storybook/addon-interactions"),
  ],
  framework: {
    name: getAbsolutePath("@storybook/react-vite"),
    options: {},
  },
  docs: {
    autodocs: "tag",
  },
  core: {},

  async viteFinal(config, {configType}) {
    const {mergeConfig} = await import("vite");

    return mergeConfig(config, {
      define: {"process.env": {}},
      plugins: [tsconfigPaths()],
      resolve: {
        alias: [
          // {
          //   find: "ui",
          //   replacement: join(__dirname, "../../../packages/ui/"),
          // }
        ],
      },
    });
  },

  staticDirs: ["../public", "../storybook-static"],
};
export default config;
