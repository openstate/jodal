import { sveltekit } from "@sveltejs/kit/vite";
import tailwindcss from "@tailwindcss/vite";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [sveltekit(), tailwindcss()],

  assetsInclude: ["**/*.md"],
  server: {
    port: 3000,
    hmr: {
      host: "app.bron.live",
    },
    fs: {
      allow: ["static"],
    },
  },
});
