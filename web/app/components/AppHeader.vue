<!--
  AppHeader — site header: title, navigation, logged-in user, login and color mode
  On mobile, the navigation opens in a side panel on the left.
  The "Mon espace" entry only shows for a logged-in user.
  No props: the logged-in user is read through useAuth()
-->
<template>
  <UHeader
    title="PandaDev"
    mode="slideover"
    toggle-side="left"
    :menu="{ side: 'left' }"
    :toggle="{ color: 'primary', variant: 'subtle' }"
  >
    <UNavigationMenu
      :items="items"
      :ui="LINK_UI"
      aria-label="Navigation principale"
    />
    <template #right>
      <template v-if="isAuthenticated">
        <UserInfo />
        <UButton
          icon="i-lucide-log-out"
          color="neutral"
          variant="ghost"
          aria-label="Se déconnecter"
          @click="logout"
        />
      </template>
      <UButton
        v-else
        label="Connexion"
        icon="i-lucide-log-in"
        color="neutral"
        variant="ghost"
        to="/login"
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
        aria-label="Navigation mobile"
      />
    </template>
  </UHeader>
</template>

<script lang="ts" setup>
import type { NavigationMenuItem } from '@nuxt/ui'

const { isAuthenticated, logout } = useAuth()

const items = computed<NavigationMenuItem[]>(() => [
  { label: 'Portfolio', icon: 'i-lucide-house', to: '/' },
  ...(isAuthenticated.value ? [{ label: 'Mon espace', icon: 'i-lucide-user-pen', to: '/admin' }] : [])
])

// Links and icons turn primary on hover (main menu and mobile menu)
const LINK_UI = { link: 'hover:text-primary', linkLeadingIcon: 'group-hover:text-primary' }
</script>
