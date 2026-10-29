<!--
  Public portfolio page of Mathias Garaios
-->
<template>
  <UContainer>
    <UPageHero
      title="test"
      :description="t('home.description')"
    />
  </UContainer>
</template>

<script setup lang="ts">
const { t } = useI18n()
definePageMeta({ layout: 'mathias-garaios' })
</script>
