<!--
  Public projects page of the portfolio
-->
<template>
  <UContainer>
    <UPageHero
      title="PandaDev Projects"
      :description="t('projects.description')"
    />
  </UContainer>
</template>

<script setup lang="ts">
const { t } = useI18n()
</script>
