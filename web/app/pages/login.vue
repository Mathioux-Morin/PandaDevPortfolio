<!--
  Login to the private area with the login and password stored in the database
-->
<template>
  <div class="flex min-h-[calc(100vh-var(--ui-header-height))] items-center justify-center p-4">
    <UAuthForm
      :schema="schema"
      :fields="fields"
      :loading="loading"
      :title="t('login.title')"
      :description="t('login.description')"
      icon="i-lucide-log-in"
      :submit="{ label: t('login.submit') }"
      class="w-full max-w-sm"
      @submit="onSubmit"
    />
  </div>
</template>

<script setup lang="ts">
import * as zod from 'zod'
import type { FormSubmitEvent } from '@nuxt/ui'

const { t, te } = useI18n()
const localePath = useLocalePath()

// Replaces zod's message with our translated one (a function, so it follows the active locale)
// for the cases handled here: missing value and empty string. Any other case shows zod's message.
const loginRequired = () => t('login.validation.loginRequired')
const passwordRequired = () => t('login.validation.passwordRequired')

const schema = zod.object({
  login: zod.string({ error: loginRequired }).min(1, { error: loginRequired }),
  password: zod.string({ error: passwordRequired }).min(1, { error: passwordRequired })
})

// Computed so that labels follow the active locale
const fields = computed(() => [
  {
    name: 'login',
    type: 'text' as const,
    label: t('login.fields.login'),
    placeholder: t('login.fields.loginPlaceholder'),
    autocomplete: 'username',
    required: true
  },
  {
    name: 'password',
    type: 'password' as const,
    label: t('login.fields.password'),
    placeholder: t('login.fields.passwordPlaceholder'),
    autocomplete: 'current-password',
    required: true
  }
])

type Schema = zod.output<typeof schema>

const loading = ref(false)
const toast = useToast()
const { refresh } = useAuth()

async function onSubmit(event: FormSubmitEvent<Schema>) {
  loading.value = true
  try {
    await $fetch('/api/auth/login', { method: 'POST', body: event.data })
    await refresh()
    await navigateTo(localePath('/admin'))
  } catch (error) {
    // The server returns an error code (invalid_credentials…), translated here
    const code = (error as { data?: { data?: { code?: string } } }).data?.data?.code
    const messageKey = code && te(`login.errors.${code}`) ? `login.errors.${code}` : 'login.errors.unknown'
    toast.add({ title: t('login.failed'), description: t(messageKey), color: 'error' })
  } finally {
    loading.value = false
  }
}
</script>
