import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  css: {
    postcss: {
      plugins: [
        require('tailwindcss'),
        require('autoprefixer'),
      ]
    }
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      'vue': 'vue/dist/vue.esm-bundler.js'
    }
  },
  build: {
    rollupOptions: {
      input: {  
        home: 'src/HomeV13.vue',
        new: 'src/NewV3.vue',
        search: 'src/SearchV1.vue',
        rules: 'src/RulesV1.vue',
        settings: 'src/SettingsV1.vue',
        WideNavbar: 'src/components/Navbar8.vue',
        TinyNavbar: 'src/components/Navbar7.vue',
        SeeMail: 'src/components/SeeMail.vue',
        Searchbar: 'src/components/SearchbarV2.vue',
        SearchContact: 'src/components/SearchContact.vue',
        SearchType: 'src/components/SearchType.vue',
        SettingsColor: 'src/components/SettingsColor.vue',
        SettingsTheme: 'src/components/SettingsTheme.vue'

      }
    }
  }
})

