declare module '#auth-utils' {
  // Data visible in the browser
  interface User {
    login: string
  }
  // Data kept on the Nuxt server, never sent to the browser
  interface SecureSessionData {
    token: string
  }
}

export {}
