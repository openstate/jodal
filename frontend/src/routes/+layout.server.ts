// Passes the user session from the server to the client.
// See `src/hooks.server.ts`.
export async function load(e) {
  return { identity: e.locals.identity };
}
