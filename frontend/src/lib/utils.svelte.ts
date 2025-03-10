import type { SubmitFunction } from "@sveltejs/kit";

export function debounce<T extends unknown[]>(
  fn: (...args: T) => void,
  ms: number,
) {
  let timeout: NodeJS.Timeout;
  return (...args: T) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(...args), ms);
  };
}

/**
 * @example createSearchQuery({ a: "b", c: 1, d: true }) // returns "a=b&c=1&d=true"
 */
export function createSearchQuery<
  const T extends Record<string, string | number | boolean>,
>(options: T) {
  return Object.entries(options)
    .map(([key, value]) => key + "=" + encodeURIComponent(value))
    .join("&");
}

/**
 * @example ```svelte
 * <script>
 *   const state = createFormState() // do not destructure
 * </script>
 *
 * <form use:enhance={state.submit}>
 *   <button disabled={state.loading}>Submit</button>
 * </form>
 * ```
 */
export function createFormState() {
  let loading = $state(false);

  const submit: SubmitFunction = () => {
    loading = true;
    return async ({ update }) => {
      await update();
      loading = false;
    };
  };

  return {
    submit,
    get loading() {
      return loading;
    },
  };
}
