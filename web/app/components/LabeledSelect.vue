<!--
  LabeledSelect — dropdown (USelect) with a label above it
  Its width fits the longest option, placeholder included.
  Props:
    label       — label shown above the dropdown
    items       — options: strings, or { label, value } objects
    placeholder — text shown when nothing is selected (optional)
  v-model — selected value
-->
<template>
  <UFormField
    :label="label"
    class="min-w-0 max-w-full"
    :ui="{ label: 'whitespace-nowrap' }"
  >
    <!-- 1×1 grid: the invisible sizer and the USelect share the same cell,
         which therefore takes the width of the longest option -->
    <div class="grid">
      <!-- pl-3 pr-10: same padding as the USelect (including room for the arrow) -->
      <span
        aria-hidden="true"
        class="invisible col-start-1 row-start-1 sm:whitespace-nowrap text-sm pl-3 pr-10"
      >{{ longestLabel }}</span>
      <USelect
        v-model="modelValue"
        :items="items"
        :placeholder="placeholder"
        class="col-start-1 row-start-1 w-full"
      />
    </div>
  </UFormField>
</template>

<script lang="ts" setup>
const props = defineProps<{
  label: string
  items: (string | { label: string, value: string })[]
  placeholder?: string
}>()

const modelValue = defineModel<string>()

// Longest label among the options and the placeholder: used as the invisible sizer
const longestLabel = computed(() => {
  const labels = props.items.map(item => typeof item === 'string' ? item : item.label)
  if (props.placeholder) labels.push(props.placeholder)
  return labels.reduce((longest, label) => label.length > longest.length ? label : longest, '')
})
</script>
