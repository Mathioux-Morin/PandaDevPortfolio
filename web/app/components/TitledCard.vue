<!--
  TitledCard — UCard with a standard header (icon + title)
  Props:
    icon  — Iconify icon name (e.g. 'i-lucide-users')
    title — title shown in the header
  Default slot: card content
-->
<template>
  <UCard>
    <template #header>
      <header class="flex items-center gap-2">
        <UIcon
          :name="icon"
          class="size-4 text-accent-11"
        />
        <h2 class="font-semibold text-highlighted">
          {{ title }}
        </h2>
      </header>
    </template>
    <slot />
  </UCard>
</template>

<script lang="ts" setup>
defineProps<{
  icon: string
  title: string
}>()
</script>
