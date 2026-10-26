export default defineNuxtRouteMiddleware((to) => {
  const { isAuthenticated } = useAuth()

  // Login page: an already logged-in user is sent to their private area
  if (to.path === '/login') {
    return isAuthenticated.value ? navigateTo('/admin', { replace: true }) : true
  }

  // Private area: logged-in users only; the portfolio stays public
  if (to.path.startsWith('/admin') && !isAuthenticated.value) {
    return navigateTo('/login', { replace: true })
  }
})
