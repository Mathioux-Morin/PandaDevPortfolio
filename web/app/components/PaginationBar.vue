<!--
  PaginationBar — centered pagination bar
  Props:
    total        — total number of items to paginate
    itemsPerPage — number of items shown per page
  v-model:page — current page (starts at 1)
-->
<template>
  <div class="flex justify-center">
    <UPagination
      v-model:page="page"
      :total="total"
      :items-per-page="itemsPerPage"
    />
  </div>
</template>

<script lang="ts" setup>
defineProps<{
  total: number
  itemsPerPage: number
}>()

const page = defineModel<number>('page', { required: true })
</script>
