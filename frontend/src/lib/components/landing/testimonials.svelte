<script lang="ts"></script>

<article class="my-30 px-6 text-stone-800">
  <h2 class="font-display mb-4 text-balance text-center text-4xl">
    Succesverhalen met Bron
  </h2>

  <div class="max-w-300 mx-auto my-16 grid gap-6 sm:grid-cols-2 md:grid-cols-3">
    {#snippet testimonial_box(
      image: string,
      name: string,
      job: string,
      testimonial: string,
    )}
      <div class="rounded-2xl border border-stone-300 px-6 py-6 transition">
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
