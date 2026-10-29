<!--
  Public portfolio page of Damien Gaetan
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
definePageMeta({ layout: 'damien-gaetan' })
</script>
