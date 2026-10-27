<!--
  UserInfo — login of the logged-in user (shown in the header)
  No props: the logged-in user is read through useAuth()
-->
<template>
  <div class="flex items-center gap-1.5 text-sm font-medium">
    <UIcon
      name="i-lucide-circle-user"
      class="size-4 text-muted"
    />
    {{ login }}
  </div>
</template>

<script lang="ts" setup>
const { t } = useI18n()
const { user } = useAuth()

// Fallback while the session does not hold a user yet
const login = computed(() => user.value?.login ?? t('user.unknown'))
</script>
