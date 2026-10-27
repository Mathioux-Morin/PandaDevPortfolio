export default defineNuxtRouteMiddleware((to) => {
  const { isAuthenticated } = useAuth()
  const localePath = useLocalePath()

  // Route name without the locale suffix (login___en → login), whatever the URL prefix
  const routeName = String(useRouteBaseName()(to) ?? '')

  // Login page: an already logged-in user is sent to their private area
  if (routeName === 'login') {
    return isAuthenticated.value ? navigateTo(localePath('/admin'), { replace: true }) : true
  }

  // Private area: logged-in users only; the portfolio stays public
  if (routeName.startsWith('admin') && !isAuthenticated.value) {
    return navigateTo(localePath('/login'), { replace: true })
  }
})
