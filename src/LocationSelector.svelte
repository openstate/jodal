<div class="multi-select-input">
   <Select items={$selectable_locations} isMulti={true} bind:selectedValue={selectedLocations} placeholder="Selecteer gemeente(s) ..."></Select>
   <HelperText>Lokatie</HelperText>
</div>

<script>
  import HelperText from '@smui/textfield/helper-text/index';
  import { addInquiry, locations, selectable_locations, id2locations, fetchingEnabled } from './stores.js';
  import { onMount, onDestroy } from 'svelte';
  //import Select, {Option} from '@smui/select';
  import Select from 'svelte-select';

  export let selectedLocations;
</script>
