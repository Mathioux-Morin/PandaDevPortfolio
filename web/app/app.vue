<template>
  <UApp :locale="uiLocale">
    <NuxtLayout>
    <NuxtPage />
    </NuxtLayout>
  </UApp>
</template>

<script setup lang="ts">
const { locale } = useI18n()

// Nuxt UI built-in texts (modals, pagination…) follow the active locale
const uiLocale = computed(() => UI_LOCALES[locale.value as UiLocaleCode])

useHead({
  htmlAttrs: {
    lang: () => uiLocale.value.code,
    dir: () => uiLocale.value.dir
  }
})
</script>
