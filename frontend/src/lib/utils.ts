import type { LocationResponse } from "./types/api";

export function debounce(fn: (value: string) => void, ms: number) {
  let timeout: NodeJS.Timeout;
  return (value: string) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(value), ms);
  };
}
