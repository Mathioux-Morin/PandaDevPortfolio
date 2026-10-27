/**
 * Authentication composable
 *
 * Provides the authentication state, the logged-in user and logout,
 * on top of nuxt-auth-utils.
 */

export const useAuth = () => {
  const { user, loggedIn, fetch } = useUserSession()
  const localePath = useLocalePath()

  const isAuthenticated = computed(() => loggedIn.value)

  // Clears the server session, refreshes the local state, then goes back to the home page
  async function logout() {
    await $fetch('/api/auth/logout', { method: 'POST' })
    await fetch()
    await navigateTo(localePath('/'))
  }

  return {
    isAuthenticated,
    user: readonly(user),

    refresh: fetch,
    logout
  }
}
