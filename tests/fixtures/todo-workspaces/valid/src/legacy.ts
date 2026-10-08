// Legacy login flow retained for old clients
// SPECKIT TODO Remove password login once OAuth migration completes
export function legacyLogin(user: string, pass: string) {
  return api.post("/login", { user, pass });
}

// Session helper
// SPECKIT TODO
// Rotate refresh tokens on every use:
// - Issue a new token pair on refresh
// - Invalidate the old pair atomically
export async function refreshSession(token: string) {
  return api.post("/refresh", { token });
}

// speckit todo — wrong case, must not open a block
//SPECKIT TODO — missing whitespace, must not open a block
export function noop() {}
