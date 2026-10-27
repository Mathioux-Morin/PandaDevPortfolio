<!--
  AppHeader — site header: title, navigation, logged-in user, login, language and color mode
  On mobile, the navigation opens in a side panel on the left.
  The "my area" entry only shows for a logged-in user.
  No props: the logged-in user is read through useAuth()
-->
<template>
  <UHeader
    title="PandaDev"
    :to="localePath('/')"
    mode="slideover"
    toggle-side="left"
    :menu="{ side: 'left' }"
    :toggle="{ color: 'primary', variant: 'subtle' }"
  >
    <UNavigationMenu
      :items="items"
      :ui="LINK_UI"
      :aria-label="t('header.mainNavigation')"
    />
    <template #right>
      <LocaleSwitcher />
      <template v-if="isAuthenticated">
        <UserInfo />
        <UButton
          icon="i-lucide-log-out"
          color="neutral"
          variant="ghost"
          :aria-label="t('header.logout')"
          @click="logout"
        />
      </template>
      <UButton
        v-else
        :label="t('header.login')"
        icon="i-lucide-log-in"
        color="neutral"
        variant="ghost"
        :to="localePath('/login')"
      />
      <UColorModeButton />
    </template>
    <!-- Side panel shown on mobile -->
    <template #body>
      <UNavigationMenu
        :items="items"
        orientation="vertical"
        class="-mx-2.5"
        :ui="LINK_UI"
        :aria-label="t('header.mobileNavigation')"
      />
    </template>
  </UHeader>
</template>

<script lang="ts" setup>
import type { NavigationMenuItem } from '@nuxt/ui'

const { t } = useI18n()
const localePath = useLocalePath()
const { isAuthenticated, logout } = useAuth()

const items = computed<NavigationMenuItem[]>(() => [
  { label: t('header.portfolio'), icon: 'i-lucide-house', to: localePath('/') },
  ...(isAuthenticated.value ? [{ label: t('header.myArea'), icon: 'i-lucide-user-pen', to: localePath('/admin') }] : [])
])

// Links and icons turn primary on hover (main menu and mobile menu)
const LINK_UI = { link: 'hover:text-primary', linkLeadingIcon: 'group-hover:text-primary' }
</script>
