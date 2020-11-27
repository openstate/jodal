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
    <Select bind:value={location} label="Lokatie">
         <Option value=""></Option>
         {#each $locations as loc}
           <Option value={loc.value} selected={location == loc.value}>{loc.label}</Option>
         {/each}
       </Select>
       <HelperText>Lokatie</HelperText>
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
  import { addInquiry, locations } from './stores.js';
  import { onMount, onDestroy } from 'svelte';
  import Select, {Option} from '@smui/select';

  let clicked = false;
  let name;
  let location;
  let query;
  let items = ['One', 'Two', 'Three'];

  function doAddInquiry() {
    addInquiry({
      name: name,
      location: location,
      query: query
    });
  }

  onMount(async () => {
      await fetch('http://api.jodal.nl/locations/search?limit=500&sort=name.keyword:asc')
        .then(r => r.json())
        .then(data => {
          console.log('got locations data:')
          console.log(data);
          items = data.hits.hits.map(function (l) {
            return {
              value: l._id,
              label: l._source.name
            };
          })
          // console.log('location items:')
          // console.dir(locationitems)
          locations.set(items)
        });
    });

  onDestroy(function () {
  });
</script>
