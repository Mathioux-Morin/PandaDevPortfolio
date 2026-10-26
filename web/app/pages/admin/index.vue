<!--
  Private area: logged-in users only (auth.global middleware)
-->
<template>
  <UContainer class="py-8">
    <TitledCard
      icon="i-lucide-user-pen"
      title="Mon espace"
    >
      <p class="text-muted">
        Connecté en tant que <span class="font-medium text-highlighted">{{ user?.login }}</span>.
        L'édition de vos données arrivera ici.
      </p>
    </TitledCard>
  </UContainer>
</template>

<script setup lang="ts">
const { user } = useAuth()
</script>
