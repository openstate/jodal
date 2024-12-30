<script lang="ts">
  import { DateInput } from "date-picker-svelte";

  type Props = { value: Date | undefined; placeholder?: string };

  let { value = $bindable(), placeholder }: Props = $props();
</script>

<DateInput
  bind:value
  placeholder={placeholder ?? new Date().toLocaleDateString("nl-NL")}
  format="dd-MM-yyyy"
  locale={{
    // prettier-ignore
    months: ["januari", "februari", "maart", "april", "mei", "juni", "juli", "augustus", "september", "oktober", "november", "december"],
    weekdays: ["zo", "ma", "di", "wo", "do", "vr", "za"],
    weekStartsOn: 1,
  }}
/>

<style>
  /* While `date-picker-svelte` has nice functionality, it comes
     with opinionated default styling. This is overridden below. */

  :global(.date-time-field) {
    display: inline-block !important;

    :global(input) {
      width: 120px !important;
      text-align: center !important;
      border: 1px solid var(--color-stone-300) !important;
      border-radius: 6px !important;
      padding: 0.5rem 1rem !important;
      font-size: 1rem !important;
      color: var(--stone-900) !important;
      background-color: white !important;
      box-shadow: none !important;
    }

    :global(.date-time-picker) {
      margin-top: 6px !important;
      border: 1px solid var(--color-stone-300) !important;
      border-radius: 6px !important;
      padding: 1rem !important;
      box-shadow: none !important;
    }
  }
</style>
