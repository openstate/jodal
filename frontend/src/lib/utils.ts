export function debounce(fn: (value: string) => void, ms: number) {
  let timeout: NodeJS.Timeout;
  return (value: string) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(value), ms);
  };
}

export function createSearchQuery<
  const T extends Record<string, string | number | boolean>,
>(options: T) {
  return Object.entries(options)
    .map(([key, value]) => key + "=" + encodeURIComponent(value))
    .join("&");
}
