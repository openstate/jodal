<script lang="ts">
  import { enhance } from "$app/forms";
  import BronLogo from "$lib/assets/bron-logo.svg?raw";
  import ArrowRight from "@tabler/icons-svelte/icons/arrow-right";

  let { data } = $props();
</script>

<header class="h-190 relative overflow-hidden">
  <enhanced:img
    src="../../lib/assets/hero.png?quality=90"
    sizes="min(1280px, 100vw)"
    fetchpriority="high"
    class="absolute inset-x-0 h-full w-full object-cover"
  />
  <div
    class="max-w-280 absolute left-1/2 top-0 mx-auto w-full -translate-x-1/2 p-4"
  >
    <nav
      class="flex w-full items-center justify-between rounded-full bg-white p-3"
    >
      <a href="/" class="px-5">
        {@html BronLogo}
      </a>
      <div class="flex gap-2 text-lg">
        <a
          href="/inloggen"
          class="flex items-center rounded-full border-2 border-stone-200 px-5 py-2 text-stone-800 transition hover:bg-stone-50"
        >
          Inloggen
        </a>
        <a
          href="/registreren"
          class="flex items-center rounded-full bg-stone-900 px-6 py-2 font-semibold text-white transition hover:bg-stone-800"
        >
          Maak gratis account
        </a>
      </div>
    </nav>
  </div>
  <div class="absolute top-24 w-full py-36 text-center">
    <h1 class="font-display mb-8 text-pretty text-6xl text-white">
      Superkrachten voor journalisten
    </h1>
    <h2 class="text-pretty text-2xl text-stone-100/80">
      Doorzoek meer dan 2 miljoen overheidsdocumenten op één plek.
    </h2>
    <form
      action="/zoeken"
      class="max-w-150 focus-within:outline-3 mx-auto mt-16 flex items-center justify-between rounded-full bg-white text-lg focus-within:outline-white/50"
    >
      <input
        type="search"
        name="zoek"
        placeholder="Zoek over elk onderwerp..."
        class="pb-4.5 w-full px-8 py-4 text-xl placeholder:text-stone-400 focus:outline-0"
      />
      <button
        class="mx-2 flex h-12 w-12 shrink-0 cursor-pointer items-center justify-center rounded-full bg-stone-900 text-white transition hover:bg-stone-800"
      >
        <ArrowRight />
      </button>
    </form>
    <div
      class="max-w-120 max-h-23 mx-auto mt-6 flex flex-wrap justify-center gap-3 overflow-y-hidden"
    >
      {#each data.examples as example}
        <a
          href="/zoeken?zoek={example.query}"
          class="flex h-10 items-center rounded-full border border-white/40 bg-white/30 px-4 py-2 font-medium text-white backdrop-blur-sm transition hover:bg-white/35"
        >
          {example.name}
        </a>
      {/each}
    </div>
  </div>
</header>

<article class="bg-stone-900 text-lg text-white">
  <p class="max-w-200 mx-auto text-pretty py-14 text-center">
    Journalisten zijn de waakhonden van onze democratie, maar de versnipperde
    toegang tot overheidsinformatie brengt kwaliteitsjournalistiek in gevaar.
    Bron verandert dat. Wij zorgen voor een revolutie in hoe informatie
    toegankelijk wordt gemaakt.
  </p>
</article>

<main class="text-stone-800">
  <article class="my-30 px-4">
    <h2 class="font-display mb-4 text-center text-4xl">
      Onderzoek nieuwe onderwerpen
    </h2>
    <h3 class="max-w-150 mx-auto text-center text-xl text-stone-500">
      Ontdek nieuwe onderwerpen en abonneer je op gecureerde feeds
    </h3>

    <div class="max-w-300 mx-auto my-16 grid grid-cols-3 gap-6">
      {#snippet explore_box(
        image: string,
        slug: string,
        title: string,
        description: string,
        tag: string,
      )}
        <a
          href="/gids/{slug}"
          class="group flex flex-col rounded-2xl border-2 border-stone-200 transition hover:bg-stone-100"
        >
          <div class=" rounded-t-2xl bg-blue-600">
            <img
              src={image}
              alt={title}
              class="h-32 w-full rounded-t-2xl object-cover opacity-75 transition group-hover:opacity-90"
              loading="lazy"
            />
          </div>
          <div class="p-8 pb-0">
            <h4 class="font-display mb-2 text-xl font-medium">{title}</h4>
            <p class="mb-4 text-stone-700">
              {description}
            </p>
          </div>
          <div class="mx-8 mb-8 flex grow items-end">
            <div
              class="w-fit rounded-full bg-blue-200 px-3 py-0.5 text-blue-900"
            >
              {tag}
            </div>
          </div>
        </a>
      {/snippet}

      {@render explore_box(
        "https://images.unsplash.com/photo-1550504630-cc20eca3b23e?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "gezondheidszorg",
        "Wachtlijsten in de GGZ",
        "Hoe lang zijn GGZ wachtlijsten in jouw regio? Zitten er grote verschillen tussen wachttijden, en zo ja, waarom?",
        "Gezondheidszorg",
      )}

      {@render explore_box(
        "https://images.unsplash.com/photo-1535379453347-1ffd615e2e08?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "landbouw",
        "Stikstofcrisis",
        "Hoe gaan gemeenten en provincies om met de stikstofproblematiek? En hoe gaat het met de regionale stikstofdoelen?",
        "Landbouw",
      )}

      {@render explore_box(
        "https://images.unsplash.com/photo-1504275107627-0c2ba7a43dba?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "lerarentekort",
        "Lerarentekort",
        "Welk effect heeft het lerarenterkort op scholen in jouw regio en wat doen schoolbesturen er aan?",
        "Onderwijs",
      )}
    </div>
  </article>

  <article class="my-30 px-4">
    <h2 class="font-display mb-4 text-center text-4xl">
      Succesverhalen met Bron
    </h2>

    <div class="max-w-300 mx-auto my-16 grid grid-cols-3 gap-6">
      {#snippet testimonial_box(
        image: string,
        name: string,
        job: string,
        testimonial: string,
      )}
        <div class="rounded-2xl border-2 border-stone-200 px-6 py-6 transition">
          <div class="mb-4 flex items-center gap-4">
            <img
              src={image}
              alt={name}
              class="h-14 w-14 rounded-full object-cover"
              loading="lazy"
            />
            <div>
              <p class="font-bold">{name}</p>
              <p class="text-stone-500">{job}</p>
            </div>
          </div>
          <p>{testimonial}</p>
        </div>
      {/snippet}

      {#each { length: 6 }}
        {@render testimonial_box(
          "https://openstate.eu/wp-content/uploads/sites/14/2023/10/portret-jan-310x310.png",
          "Jan van der Burgt",
          "Journalist",
          "Bron bundelt alles wat ik nodig heb op één plek. Geen gedoe meer met versnipperde informatie – ik kan direct aan de slag. Onmisbaar voor elke journalist!",
        )}
      {/each}
    </div>
  </article>

  <article class="my-30 px-4">
    <h2 class="font-display mb-4 text-center text-4xl">
      Mis nooit meer dat ene document
    </h2>

    <h3 class="max-w-150 mx-auto mb-12 text-center text-xl text-stone-500">
      Stel geavanceerde zoekopdrachten in en ontvang nieuwe zoekresultaten in je
      e-mail. Maak een account aan.
    </h3>

    <a
      href="/registreren"
      class="mx-auto mb-4 flex w-fit items-center rounded-full bg-stone-900 px-6 py-3 text-xl font-semibold text-white transition hover:bg-stone-800"
    >
      Maak een gratis account aan
    </a>

    <p class="text-center text-stone-500">Exclusief voor journalisten</p>
  </article>
</main>

<footer class="bg-stone-900 py-24 rounded-t-3xl text-white">
  <div class="max-w-300 mx-auto">
    <div class="mb-12 grid grid-cols-[1fr_25rem]">
      <a href="/" class="space-y-4">
        {@html BronLogo}
        <span class="text-stone-400 text-lg">Superkrachten voor journalisten</span>
      </a>
      <div class="flex flex-col font-semibold gap-2">
        <a href="/over">Over Bron</a>
        <a href="/contact">Contact</a>
        <a href="/github">GitHub</a>
      </div>
    </div>
    <p class="text-stone-400">
      De content op deze site is beschikbaar onder de licentie
      <a
        href="https://creativecommons.org/licenses/by-sa/4.0/deed.nl"
        target="_blank"
        class="underline"
      >
        Creative Commons Naamsvermelding/Gelijk delen
      </a>, er kunnen aanvullende voorwaarden van toepassing zijn. Zie de
      gebruiksvoorwaarden voor meer informatie. Bron is onderdeel van
      <a href="https://openstate.eu/nl" target="_blank" class="underline">
        Open State Foundation
      </a>, een organisatie zonder winstoogmerk.
    </p>
  </div>
</footer>
