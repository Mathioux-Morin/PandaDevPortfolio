<!--
  ConfirmModal — modal (UModal) asking to confirm an action before running it
  Props:
    title        — modal title (e.g. 'Confirmer la suppression')
    description  — question asked (optional, e.g. « Supprimer ce projet ? »)
    confirmLabel — label of the confirm button; default: 'Confirmer'
    color        — color of the confirm button: NuxtUiColor, default 'error' (risky action)
  v-model:open — modal open or closed; "Annuler", Escape or a click outside close it
  Emits: confirm when the confirm button is clicked, then the modal closes
-->
<template>
  <UModal
    v-model:open="isOpen"
    :title="title"
    :description="description"
    :ui="{ footer: 'justify-end' }"
  >
    <template #footer>
      <UButton
        label="Annuler"
        color="neutral"
        variant="outline"
        @click="isOpen = false"
      />
      <UButton
        :label="confirmLabel"
        :color="color"
        @click="confirm"
      />
    </template>
  </UModal>
</template>

<script lang="ts" setup>
// Props described in the header; defaults: no description, red "Confirmer" button
withDefaults(defineProps<{
  title: string
  description?: string
  confirmLabel?: string
  color?: NuxtUiColor
}>(), {
  description: undefined,
  confirmLabel: 'Confirmer',
  color: 'error'
})

// "confirm" tells the page the action is approved; the page runs it
const emit = defineEmits<{ confirm: [] }>()

// Modal open or closed, bound to the page through v-model:open
const isOpen = defineModel<boolean>('open', { default: false })

// Confirm button click: notify the page, then close the modal
function confirm() {
  emit('confirm')
  isOpen.value = false
}
</script>
