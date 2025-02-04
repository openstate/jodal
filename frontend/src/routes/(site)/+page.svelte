<script lang="ts">
  import LandingHero from "$lib/components/landing/hero.svelte";
  import LandingTagline from "$lib/components/landing/tagline.svelte";
  import LandingExplanation from "$lib/components/landing/explanation.svelte";
  import LandingExplore from "$lib/components/landing/explore.svelte";
  // import LandingTestimonials from "$lib/components/landing/testimonials.svelte";
  import LandingCTA from "$lib/components/landing/cta.svelte";

  let { data } = $props();
</script>

<LandingHero examples={data.examples} />
<LandingTagline />
<LandingExplanation />
<LandingExplore articles={data.articles} />
<!-- <LandingTestimonials /> -->
<LandingCTA />
