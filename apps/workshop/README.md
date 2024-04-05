## Getting Started

First, run the development server:

```sh
pnpm dev
```
This will automatically open a browser window with the app running on [http://localhost:6006](http://localhost:6006). To add more components
to the app, create a new file with the `.stories.tsx` extension. The storybook will automatically pick up the new file
and add the component to the storybook.

## Known Issues

- There is currently a build issue with the `@repo/ui` packages not automatically building tailwind css when updated. To
    fix this, run the following command in the `@repo/ui` package:

  ```sh
  pnpm build
  ```