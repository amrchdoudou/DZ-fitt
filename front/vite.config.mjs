import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    watch: { usePolling: true },
    allowedHosts: [
      '972adeb4dade.ngrok-free.app', // your ngrok URL
      'localhost',                    // always keep localhost
    ],
    strictPort: true, // optional, ensures port 5173 is used
  },
});