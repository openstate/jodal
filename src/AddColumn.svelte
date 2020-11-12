<Dialog bind:this={simpleDialog} aria-labelledby="simple-title" aria-describedby="simple-content">
  <!-- Title cannot contain leading whitespace due to mdc-typography-baseline-top() -->
  <Title id="add-column-title">Toevoegen</Title>
  <Content id="add-column-content">
    <div>
      <Textfield>
        <Input bind:value={name} id="column-name" aria-controls="helper-text-column-name" aria-describedby="helper-text-column-name" />
        <FloatingLabel for="input-column-name">Naam</FloatingLabel>
        <LineRipple />
      </Textfield>
      <HelperText id="helper-text-column-name">Een beschrijvende naam voor de zoekopdracht</HelperText>
    </div>
    <div>
      <Textfield>
        <Input bind:value={location} id="column-location" aria-controls="helper-text-column-location" aria-describedby="helper-text-column-location" />
        <FloatingLabel for="input-column-location">Lokatie</FloatingLabel>
        <LineRipple />
      </Textfield>
      <HelperText id="helper-text-column-location">De lokatie(s) voor de zoekopdracht</HelperText>
    </div>
    <div>
      <Textfield>
        <Input bind:value={query} id="column-query" aria-controls="helper-text-column-query" aria-describedby="helper-text-column-query" />
        <FloatingLabel for="input-column-name">Zoekopdracht</FloatingLabel>
        <LineRipple />
      </Textfield>
      <HelperText id="helper-text-column-name">De zoekopdracht</HelperText>
    </div>
 </Content>
 <Actions>
   <Button on:click={() => clicked = 'No'}>
     <Label>Annuleren</Label>
   </Button>
   <Button on:click={doAddInquiry}>
     <Label>Toevoegen</Label>
   </Button>
 </Actions>
</Dialog>

<script context="module">
  let simpleDialog;

	export function startAddColumn() {
    simpleDialog.open();
	}
</script>

<script>
  import Textfield, {Input, Textarea} from '@smui/textfield';
  import HelperText from '@smui/textfield/helper-text/index';
  import Dialog, {Title, Content, Actions, InitialFocus} from '@smui/dialog';
  import Button, {Label} from '@smui/button';
  import FloatingLabel from '@smui/floating-label';
  import LineRipple from '@smui/line-ripple';
  import { addInquiry } from './stores.js';

  let clicked = false;
  let name;
  let location;
  let query;

  function doAddInquiry() {
    addInquiry({
      name: name,
      location: location,
      query: query
    });
  }
</script>
