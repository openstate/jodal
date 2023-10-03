<div class="multi-select-input">
   <Select items={$selectable_locations} isMulti={true} bind:selectedValue={selectedLocations} placeholder="Selecteer gemeente(s) ..."></Select>
   {#if (showNumberOfSelectedLocations && selectedLocations)}
   <p class="locations-select-byline">Er zijn {selectedLocations.length} lokaties geselecteerd</p>
   {/if}
   {#if showEmptyButton}
   <Button align="end" variant="outlined" on:click={() => clearLocations()}><Label>Leeg maken</Label></Button>
   {/if}
</div>

<script>
  import HelperText from '@smui/textfield/helper-text/index';
  import { addInquiry, locations, selectable_locations, id2locations, fetchingEnabled } from './stores.js';
  import { onMount, onDestroy } from 'svelte';
  //import Select, {Option} from '@smui/select';
  import Select from 'svelte-select';
  import Button from '@smui/button';
  import Fab, {Label, Icon} from '@smui/fab';

  export let selectedLocations = ['*'];
  export let showEmptyButton = true;
  export let showNumberOfSelectedLocations = false;

  function handleSelect(details) {
    console.log('locations select:', details);
  }
  function selectAllLocations() {
    console.log('all locations button clicked!');
    selectedLocations = $selectable_locations;
  }

  function clearLocations() {
    console.log('All locations empty!');
    selectedLocations = [];
  }
</script>
