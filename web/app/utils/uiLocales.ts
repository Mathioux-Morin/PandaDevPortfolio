// Nuxt UI built-in texts of the locales declared in nuxt.config.ts (i18n.locales).
// Only these are imported: `import * from '@nuxt/ui/locale'` would bundle all ~60 languages.
import { en, fr } from '@nuxt/ui/locale'

export const UI_LOCALES = { en, fr }

export type UiLocaleCode = keyof typeof UI_LOCALES

// Flag icon of each locale (Iconify circle-flags collection), shown in LocaleSwitcher
export const LOCALE_FLAGS: Record<UiLocaleCode, string> = {
  fr: 'i-circle-flags-fr',
  en: 'i-circle-flags-lang-en'
}
