<!--
  LocaleSwitcher — flag button showing the active locale (shown in the header)
  A click switches to the next locale and keeps the current page: /login ↔ /en/login.
  It is a link, so it also works without JavaScript. `:locale="false"` stops Nuxt UI from
  localizing the target again into the active locale (which would turn "/" back into "/en").
  No props: the available locales come from the i18n config in nuxt.config.ts
-->
<template>
  <UButton
    :icon="LOCALE_FLAGS[locale as UiLocaleCode]"
    :to="switchLocalePath(nextLocale)"
    :locale="false"
    :aria-label="t('header.switchLanguage')"
    color="neutral"
    variant="ghost"
  />
</template>

<script lang="ts" setup>
const { t, locale, locales } = useI18n()
const switchLocalePath = useSwitchLocalePath()

// Locale that follows the active one in nuxt.config.ts (the other one, with two locales)
const nextLocale = computed(() => {
  const codes = locales.value.map(({ code }) => code)
  return codes[(codes.indexOf(locale.value) + 1) % codes.length] ?? locale.value
})
</script>
