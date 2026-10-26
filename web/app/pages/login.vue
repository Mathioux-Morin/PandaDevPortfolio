<!--
  Login to the private area with the login and password stored in the database
-->
<template>
  <div class="flex min-h-[calc(100vh-var(--ui-header-height))] items-center justify-center p-4">
    <UAuthForm
      :schema="schema"
      :fields="fields"
      :loading="loading"
      title="Connexion"
      description="Accédez à votre espace PandaDev"
      icon="i-lucide-log-in"
      :submit="{ label: 'Se connecter' }"
      class="w-full max-w-sm"
      @submit="onSubmit"
    />
  </div>
</template>

<script setup lang="ts">
import * as zod from 'zod'
import type { FormSubmitEvent } from '@nuxt/ui'

const schema = zod.object({
  login: zod.string().min(1, 'Le login est requis'),
  password: zod.string().min(1, 'Le mot de passe est requis')
})

const fields = [
  {
    name: 'login',
    type: 'text' as const,
    label: 'Login',
    placeholder: 'Votre login',
    autocomplete: 'username',
    required: true
  },
  {
    name: 'password',
    type: 'password' as const,
    label: 'Mot de passe',
    placeholder: 'Votre mot de passe',
    autocomplete: 'current-password',
    required: true
  }
]

type Schema = zod.output<typeof schema>

const loading = ref(false)
const toast = useToast()
const { refresh } = useAuth()

async function onSubmit(event: FormSubmitEvent<Schema>) {
  loading.value = true
  try {
    await $fetch('/api/auth/login', { method: 'POST', body: event.data })
    await refresh()
    await navigateTo('/admin')
  } catch (error) {
    const message = (error as { data?: { statusMessage?: string } }).data?.statusMessage
    toast.add({ title: 'Connexion impossible', description: message, color: 'error' })
  } finally {
    loading.value = false
  }
}
</script>
