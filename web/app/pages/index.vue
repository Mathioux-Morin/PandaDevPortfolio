<!--
  Public home page of the portfolio
-->
<template>
  <UContainer>
    <UPageHero
      title="PandaDev Portfolio"
      :description="t('home.description')"
    />
  </UContainer>
</template>

<script setup lang="ts">
const { t } = useI18n()
</script>
