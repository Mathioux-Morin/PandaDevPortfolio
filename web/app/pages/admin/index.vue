<!--
  Private area: logged-in users only (auth.global middleware)
-->
<template>
  <UContainer class="py-8">
    <TitledCard
      icon="i-lucide-user-pen"
      :title="t('admin.title')"
    >
      <p class="text-muted">
        <i18n-t
          keypath="admin.loggedInAs"
          tag="span"
        >
          <template #login>
            <span class="font-medium text-highlighted">{{ user?.login }}</span>
          </template>
        </i18n-t>
        {{ t('admin.comingSoon') }}
      </p>
    </TitledCard>
  </UContainer>
</template>

<script setup lang="ts">
const { t } = useI18n()
const { user } = useAuth()
</script>
