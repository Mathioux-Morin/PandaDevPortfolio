<!--
  Public about page of the portfolio
-->
<template>
  <UContainer>
    <UPageHero
      title="PandaDev About"
      :description="t('about.description')"
    />
  </UContainer>
</template>

<script setup lang="ts">
const { t } = useI18n()
</script>
