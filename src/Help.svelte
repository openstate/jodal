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

     <Accordion id="1" {openedAccordion} on:accordionSelected={toggleAccordion}>
     <span slot="title" class="valign-wrapper">
      Weten waar JODAL voor te gebruiken is?
      <span class="material-icons acc-chevron">chevron_right</span>
     </span>
     <span>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
     tempor incididunt ut labore et dolore magna aliqua.
      Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
      aliquip ex ea commodo consequat.</span>
    </Accordion>

    <Accordion  id="2" {openedAccordion}  on:accordionSelected={toggleAccordion}>
      <span slot="title" class="valign-wrapper">
        Een account aanmaken op JODAL
        <span class="material-icons acc-chevron">chevron_right</span>
      </span>
      <span>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
      tempor incididunt ut labore et dolore magna aliqua.
       Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
       aliquip ex ea commodo consequat.</span>
    </Accordion>

    <Accordion id="3" {openedAccordion}  on:accordionSelected={toggleAccordion}>
      <span slot="title" class="valign-wrapper">
        Uitleg over de hoofdpagina van JODAL
        <span class="material-icons acc-chevron">chevron_right</span>
      </span>
      <span>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
      incididunt ut labore et dolore magna aliqua.
       Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip
       ex ea commodo consequat.</span>
    </Accordion>

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
