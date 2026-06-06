import { defineConfig } from 'vite'

// Phase 1: faithful mirror of getty.edu/tracingart.
// The captured Nuxt runtime expects baseURL '/tracingart/', so we serve the
// whole app (index.html + public assets) under that base path.
export default defineConfig({
  base: '/tracingart/',
  publicDir: 'public',
  server: { host: true, port: 5173 },
})
