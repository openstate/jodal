export async function load(event) {
  const { userId: user_id, feedId: query_id } = event.params;

  const response = await event.fetch(
    "http://binoas.openstate.eu/subscriptions/delete",
    { method: "DELETE", body: JSON.stringify({ user_id, query_id }) },
  );

  console.log(response);

  return { success: response.ok };
}
