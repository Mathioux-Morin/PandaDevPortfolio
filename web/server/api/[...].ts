// Forwards every `/api/...` request not handled locally to the FastAPI API.
// The session JWT is added when the user is logged in: FastAPI alone decides
// which routes are public and which require a token.
import { joinURL } from 'ufo'

export default defineEventHandler(async (event) => {
  const { apiUrl } = useRuntimeConfig(event)
  const session = await getUserSession(event)
  const token = session.secure?.token

  const target = joinURL(apiUrl, event.path.replace(/^\/api\//, ''))

  return proxyRequest(event, target, {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
    async onResponse(event, response) {
      // Token expired or rejected: the session is no longer valid
      if (token && response.status === 401) await clearUserSession(event)
    }
  })
})
