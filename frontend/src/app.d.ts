/// <reference types="@sveltejs/kit" />

// See https://svelte.dev/docs/kit/types
// for information about these interfaces
declare namespace App {
  interface Locals {
    identity: import("$lib/stores").Identity | null;
  }

  interface PageData {
    identity: import("$lib/stores").Identity | null;
    feeds: import("$lib/types/api").FeedResponse[] | null;
  }
}
