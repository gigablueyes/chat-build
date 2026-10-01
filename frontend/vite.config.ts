import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
// `base` is configurable so the built assets resolve correctly when served
// from a GitHub Pages project site (https://<user>.github.io/<repo>/).
export default defineConfig({
  plugins: [react()],
  base: process.env.VITE_BASE_PATH ?? '/',
})
