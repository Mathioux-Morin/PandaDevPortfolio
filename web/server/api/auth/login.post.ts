// Login: exchanges login and password for a JWT from FastAPI, then opens the session
import * as zod from 'zod'
import { joinURL } from 'ufo'

interface TokenResponse {
  access_token: string
  token_type: string
}

const schema = zod.object({
  login: zod.string().min(1),
  password: zod.string().min(1)
})

export default defineEventHandler(async (event) => {
  const { login, password } = await readValidatedBody(event, schema.parse)
  const { apiUrl } = useRuntimeConfig(event)

  let token: TokenResponse
  try {
    token = await $fetch<TokenResponse>(joinURL(apiUrl, '/auth/token'), {
      method: 'POST',
      body: { login, password }
    })
  } catch (error) {
    // `data.code` is translated by the login page (i18n/locales/*.json → login.errors)
    if ((error as { statusCode?: number }).statusCode === 401) {
      throw createError({ statusCode: 401, statusMessage: 'Invalid credentials', data: { code: 'invalid_credentials' } })
    }
    throw createError({ statusCode: 502, statusMessage: 'API unavailable', data: { code: 'api_unavailable' } })
  }

  // The JWT stays in the `secure` part of the session: it is never exposed to the browser
  await replaceUserSession(event, {
    user: { login },
    secure: { token: token.access_token }
  })

  return { login }
})
