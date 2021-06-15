<script>
  import Textfield, {Input, Textarea} from '@smui/textfield';
  import HelperText from '@smui/textfield/helper-text/index';
  import Dialog, {Title, Content, Actions, InitialFocus} from '@smui/dialog';
  import Button, {Label} from '@smui/button';
  import FloatingLabel from '@smui/floating-label';
  import LineRipple from '@smui/line-ripple';
  import { addInquiry, locations, selectable_locations, id2locations, fetchingEnabled } from './stores.js';
  import { onMount, onDestroy } from 'svelte';
  //import Select, {Option} from '@smui/select';
  import Select from 'svelte-select';

  let clicked = false;
  let name;
  let location;
  let selectLocation;
  let query;
  let items = ['One', 'Two', 'Three'];
  let _id2locations = {};
  let selectedLocations;

  function doAddInquiry() {
    console.dir('selected locations:');
    console.log(selectedLocations);
    var selected_ids = selectedLocations.map(function (l) { return l.value; });
    var selected_names = selectedLocations.map(function (l) { return l.label; })
    // TODO: Supprt adding multiple locations in a single column
    var selected = $locations.filter(l => selected_ids.indexOf(l.id) >= 0);
    if (name == '') {
      name = selected_names.join(", ");
    }
    if (query == '') {
      query = "*"
    }
    console.log('adding name:' + name);
    console.log('adding selected : ');
    console.dir(selected);
    // TODO: maybe we should do this async?
    addInquiry({
      name: name,
      locations: selected_ids,
      user_query: query
    });
  }

  onMount(async () => {
      await fetch('//api.jodal.nl/locations/search?limit=500&sort=name.keyword:asc')
      //await fetch('https://api.jodal.nl/locations/search?limit=500&sort=name.keyword:asc')
        .then(r => r.json())
        .then(data => {
          console.log('got locations data:')
          console.log(data);
          items = data.hits.hits.map(function (l) {
            return l._source;
          })
          _id2locations = {}
          items.forEach(function (i) {
            i['sources'].forEach(function (s) {
              _id2locations[s['id']] = i['name']
            })
          })
          console.dir('id2locations:')
          console.log(_id2locations);
          id2locations.set(_id2locations);
          console.log('location items:')
          console.dir(items)
          locations.set(items)
          console.log('selectable locations:')
          console.dir($selectable_locations)
          console.log('setting fetching to enabled!')
          fetchingEnabled.set(true)
        });
    });

  onDestroy(function () {
  });
</script>

<Dialog bind:this={simpleDialog} aria-labelledby="simple-title" aria-describedby="simple-content">
  <!-- Title cannot contain leading whitespace due to mdc-typography-baseline-top() -->
  <Title id="add-column-title">Toevoegen</Title>
  <Content id="add-column-content">
    <div>
      <Textfield>
        <Input bind:value={name} id="column-name" aria-controls="helper-text-column-name" aria-describedby="helper-text-column-name" />
        <FloatingLabel for="input-column-name">Kolom naam</FloatingLabel>
        <LineRipple />
      </Textfield>
      <HelperText id="helper-text-column-name">Een beschrijvende naam voor de zoekopdracht</HelperText>
    </div>
    <div class="multi-select-input">
       <Select items={$selectable_locations} isMulti={true} bind:selectedValue={selectedLocations} placeholder="Selecteer gemeente(s) ..."></Select>
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

<style>
</style>
