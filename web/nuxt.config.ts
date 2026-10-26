export default defineNuxtConfig({
  modules: [
    '@nuxt/ui',
    '@nuxt/eslint',
    'nuxt-auth-utils'
  ],

  devtools: {
    enabled: true
  },

  app: {
    head: {
      title: 'PandaDev Portfolio',
      htmlAttrs: {
        lang: 'fr'
      },
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' }
      ],
      noscript: [
        { textContent: 'JavaScript is required' }
      ]
    }
  },

  css: ['~/assets/css/main.css'],

  colorMode: {
    preference: 'system',
    fallback: 'dark',
    classSuffix: ''
  },

  ui: {
    theme: {
      transitions: true,
      defaultVariants: {
        color: 'primary',
        size: 'md'
      },
      colors: [
        'primary', 'secondary', 'info', 'success', 'warning', 'error',
        'violet', 'pink', 'orange', 'teal', 'cyan', 'rose', 'indigo', 'lime', 'fuchsia', 'purple'
      ]
    },
    experimental: {
      componentDetection: true
    }
  },

  runtimeConfig: {
    // FastAPI URL, overridden by NUXT_API_URL
    apiUrl: 'http://127.0.0.1:8000',
    session: {
      password: process.env.NUXT_SESSION_PASSWORD || '',
      cookie: {
        sameSite: 'lax',
        secure: process.env.NODE_ENV === 'production'
      }
    }
  },

  compatibilityDate: '2025-01-15',

  vite: {
    // Dependencies pre-bundled at startup: otherwise Vite discovers them when a page using them
    // first loads (zod on the login page, the devtools) and reloads the page
    optimizeDeps: {
      include: ['zod', '@vue/devtools-core']
    }
  },

  typescript: {
    tsConfig: {
      compilerOptions: {
        types: ['node']
      }
    }
  },

  eslint: {
    config: {
      stylistic: {
        commaDangle: 'never',
        braceStyle: '1tbs'
      }
    }
  }
})
