<style>
  .acc-header {
    width: 100%;
  }
</style>

<Dialog
  bind:open
  bind:this={helpDialog}
  aria-labelledby="default-focus-title"
  aria-describedby="default-focus-content"
  class="help-dialog"
>
  <Title id="default-focus-title">Help</Title>
  <Content id="default-focus-content">
  <div class="container">

  <Accordions>

    {#each questions as question}
     <Accordion id="{question.id}" {openedAccordion} on:accordionSelected={toggleAccordion}>
     <span slot="title" class="valign-wrapper">
      {question.question}
      <span class="material-icons acc-chevron">chevron_right</span>
     </span>
     <span>
      <iframe src="{question.video}" width="640" height="320" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe>
      <p>{question.description}</p>
    </span>
    </Accordion>
    {/each}
  </Accordions>
  </div>
  </Content>
  <Actions>
    <Button
      default
      use={[InitialFocus]}
      on:click={() => (response = 'It will be glorious.')}
    >
      <Label>Sluiten</Label>
    </Button>
  </Actions>
</Dialog>

<script>
  import Dialog, { Title, Content, Actions, InitialFocus } from '@smui/dialog';
  import Button, { Label } from '@smui/button';
  import { Accordions, Accordion } from "./Accordion";

  let open;
  let response = 'Nothing yet.';

  // https://player.vimeo.com/video/606390974
  let questions = [
    {
      id: 1,
      question: "Weten wat JODAL voor te gebruiken is?",
      video: "https://player.vimeo.com/video/606390896",
      description: "Wil je meer weten over hoe het platform en hoe JODAL jou kan helpen bij het doen van onderzoek? Bekijk deze video."
    },
    {
      id: 2,
      question: "Een account aanmaken",
      video: "https://player.vimeo.com/video/606390855",
      description: "JODAL is een gepersonaliseerde omgeving. Wil je uitleg over hoe je een eigen account aanmaakt? Bekijk deze video."
    },
    {
      id: 3,
      question: "Uitleg over de hoofdpagina",
      video: "https://player.vimeo.com/video/606390896",
      description: "De hoofdpagina van JODAL is jouw gepersonaliseerde dashboard. Meer weten over hoe dit werkt? Bekijk deze video."
    },
    {
      id: 4,
      question: "Een nieuwe zoekopdracht aanmaken",
      video: "https://player.vimeo.com/video/606391507",
      description: "Wil je weten hoe je een nieuwe zoekopdracht aanmaakt? Bekijk deze video."
    },
    {
      id: 5,
      question: "Een zoekopdracht aanpassen",
      video: "https://player.vimeo.com/video/606390974",
      description: "Wil je weten hoe je een bestaande zoekopdracht kan aanpassen, verfijnen of verwijderen? Bekijk deze video."
    },
    {
      id: 6,
      question: "Een bron vinden",
      video: "https://player.vimeo.com/video/606391074",
      description: "Jouw gepersonaliseerde zoekresultaten komen van verschillende bronnen. Meer weten over hoe je bij de juiste bron komt? Bekijk deze video."
    },
    {
      id: 7,
      question: "Uitleg over het hergebruiken van informatie",
      video: "https://player.vimeo.com/video/606391313",
      description: "Mocht je vragen hebben over het platform of andere data-vragen dan kan je terecht bij onze helpdesk. Bekijk deze video voor meer informatie."
    },
    {
      id: 8,
      question: "Meer weten over je account en privacy",
      video: "https://player.vimeo.com/video/606391199",
      description: "Uitleg over het beheren van je account en privacy vind je in deze video."
    },
  ];
  // opened Accordion
  let openedAccordion = 0;
  const toggleAccordion = e =>
    (openedAccordion = e.detail == openedAccordion ? 0 : e.detail);
</script>

<script context="module">
  let helpDialog;

	export function showHelpDialog() {
    helpDialog.open();
	}
</script>
