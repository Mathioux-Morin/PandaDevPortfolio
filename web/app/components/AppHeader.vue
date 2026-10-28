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
    :ui="{
      root: `top-4 mx-auto w-[calc(100%-2rem)] max-w-6xl rounded-full border border-gray-6 bg-gray-1 shadow-md`,
      header: `px-4 sm:px-6`
    }"
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
  { label: t('header.projects'), icon: 'i-lucide-folder', to: localePath('/projects') },
  { label: t('header.about'), icon: 'i-lucide-info', to: localePath('/about') },
  ...(isAuthenticated.value ? [{ label: t('header.myArea'), icon: 'i-lucide-user-pen', to: localePath('/admin') }] : [])
])

// Links and icons take the accent text color on hover (main menu and mobile menu)
const LINK_UI = { link: ' rounded-lg bg-gray-1 hover:bg-accent-3 hover:text-accent-12', linkLeadingIcon: 'group-hover:text-accent-12' }
</script>
