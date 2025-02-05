import { sveltekit } from "@sveltejs/kit/vite";
import tailwindcss from "@tailwindcss/vite";
import { enhancedImages } from "@sveltejs/enhanced-img";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [enhancedImages(), sveltekit(), tailwindcss()],
  assetsInclude: ["**/*.md"],
  server: {
    port: 3000,
    hmr: {
      host: "bron.live",
    },
    fs: {
      allow: ["static"],
    },
  },
});
