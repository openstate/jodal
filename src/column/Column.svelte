<script>
import { onMount, onDestroy } from 'svelte';
import Entry from './Entry.svelte';
import Button from '@smui/button';
import IconButton from '@smui/icon-button';
import Textfield from '@smui/textfield'
import { writable, get, derived } from 'svelte/store';
import { sources, locations, inquiries, fetchingEnabled, removeInquiry, isTesting } from '../stores.js';
import { fetchSource } from '../sources.js';
import Checkbox from '@smui/checkbox';
import FormField from '@smui/form-field';
import { fade, slide } from 'svelte/transition';
import Fab, {Label, Icon} from '@smui/fab';
import orderBy from 'lodash/orderBy';
import { showDocumentDialog } from '../Document.svelte';
import { showSearchHelpDialog } from '../SearchHelp.svelte';
import Select, {Option} from '@smui/select';
import HelperText from '@smui/select/helper-text/index';
import Flatpickr from '../Flatpickr.svelte';
import { Dutch } from "flatpickr/dist/l10n/nl.js"
import FloatingLabel from '@smui/floating-label';
import LocationSelector from '../LocationSelector.svelte';

export let inquiry;

let column_locations = [];
let last_length=0;
let start=0;
let end=5;

let items_ = writable([]);
let items = derived(items_, (items_) => orderBy(items_, [(inquiry.sort == 'published') ? 'date' : '_score'], [inquiry.sort_order]))
let item_ids = {};
let empty = false;
let query = inquiry.user_query;
let column_id = inquiry.id;
let show_settings = false;
let show_marker = false;
let scroll_marker;
let virtual_list;
let show_sources = true;
let loading = true;
let hidden = false;
let stable_date = undefined;
let stable_page_number = 1;
let old_source_counts = writable({});
let source_counts = writable({});
let orderField = inquiry.sort;
let orderWay = inquiry.sort_order;
let selectedLocations = [];
let startDateValue = inquiry.date_start ? new Date(Date.parse(inquiry.date_start)) : '';
let startDateFormattedValue = '';
let endDateValue = inquiry.date_start ? new Date(Date.parse(inquiry.date_end)) : '';
let endDateFormattedValue = '';
let columnName = inquiry.name;
let itemsLeft = true;

const startDateOptions = {
	enableTime: false,
  element: '#start-picker-' + column_id,
  locale: Dutch,
  defaultHour: 0,
  defaultMinute: 0,
  defaultDate: startDateValue,
	onChange(selectedDates, dateStr) {
		console.log('flatpickr hook', selectedDates, dateStr);
	}
};
const endDateOptions = {
	enableTime: false,
  element: '#end-picker-' + column_id,
  locale: Dutch,
  defaultHour: 0,
  defaultMinute: 0,
  defaultDate: endDateValue,
	onChange(selectedDates, dateStr) {
		console.log('flatpickr hook', selectedDates, dateStr);
	}
};

console.log('sdo: ', startDateOptions);

function prepareSettings() {
	console.log('inquiry locations: ', inquiry.locations);
	console.log('inquiry filtering locations: ', $locations.length);
	selectedLocations =  $locations.filter(l => inquiry.locations.indexOf(l.id) >= 0).map(function (l) { return {value: l.id, label: l.name};});
	console.log('inquiry  selected', selectedLocations);
};

function handleStartDateChange(event) {
	const [ selectedDates, dateStr, fpInstance ] = event.detail;
	console.log({ selectedDates,  dateStr });
  if (selectedDates.length > 0) {
    startDateValue = selectedDates[0].toISOString();
    startDateFormattedValue = dateStr;
  } else {
    startDateValue = '';
    startDateFormattedValue = '';
  }
  fpInstance.close();
}

function handleEndDateChange(event) {
	const [ selectedDates, dateStr, fpInstance ] = event.detail;
	console.log({ selectedDates,  dateStr });
  if (selectedDates.length > 0) {
    endDateValue = selectedDates[0].toISOString();
    endDateFormattedValue = dateStr;
  } else {
    endDateValue = '';
    endDateFormattedValue = '';
  }
  fpInstance.close();
}

function handleStartDateSubmit(event) {
	event.preventDefault();

	console.log(event.target.elements['date'].value);
}

function getLocations() {
  column_locations = $locations.filter((l) => inquiry.locations.includes(l.id));
}

function shuffle(array) {
  var currentIndex = array.length, temporaryValue, randomIndex;

  // While there remain elements to shuffle...
  while (0 !== currentIndex) {

    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;

    // And swap it with the current element.
    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }

  return array.map(function (i) {return i;});
}

function doSomething() {
  console.log('toggling settings!');
   show_settings = !show_settings;
	 if (show_settings) {
		 prepareSettings();
	 }
 }

function doGoToEntry() {
  show_marker = false;
  if (scroll_marker) {
    var column_id = "column-contents-" + inquiry.order;
    var entry_name = 'entry_' + inquiry.order + scroll_marker;
    //console.log(entry_name);
    var myElement = document.getElementById(entry_name);
    var topPos = myElement.offsetTop;
    console.log('entry ' + entry_name + ' is at ' + topPos);
    // console.log('Should move column ' + inquiry.order + 'to position ' + topPos + 'now!');
    document.getElementById(column_id).scrollTop = topPos;
  }
}

function doNextPage() {
  console.log('should get next page with stable ' + stable_date + ' with page ' + stable_page_number);
  loading = true;
  fetchFromSources(stable_page_number, stable_date);
  stable_page_number += 1;
}

function getFocus() {
  var count = $items.length;
  console.log('got focus! resulted in  ' + (count - last_length) + ' new $items');
  show_marker =  ((count-last_length) > 0); //(end - start);
  last_length = count;

}

function loseFocus() {
  var count = $items.length;
  //scroll_marker = virtual_list.$items[start];
  if (count > 0) {
    console.log('Lost focus in column ' + inquiry.order + '!: ' + $items[start].key);
    scroll_marker = $items[start].key;
    last_length = count;
    show_marker = false;
  }
  old_source_counts.set(source_counts);
}

function handleClosedLeading() {
  console('leadgsackar closed');
}

function removeColumn() {
  show_settings = false;
  hidden = true;
  removeInquiry(column_id);
}

function update(obj, upd/*, …*/) {
    for (var i=1; i<arguments.length; i++) {
        for (var prop in arguments[i]) {
            var val = arguments[i][prop];
            // if (typeof val == "object") // this also applies to arrays or null!
            //     update(obj[prop], val);
            // else
                obj[prop] = val;
        }
    }
    return obj;
}

function updateInquiry(updatedFields) {
	if (!get(isTesting)) {
	  var url = window.location.protocol + '//api.jodal.nl/columns/' + inquiry.id;
		console.log('query change update fields:', update(inquiry, updatedFields));
	  fetch(
	    url, {
	      method: 'POST',
	      credentials: 'include',
	      cache: 'no-cache',
	      body: JSON.stringify(update(inquiry, updatedFields)),
	      headers: new Headers({'content-type': 'application/json'})
	    }).then(
	      response => response.json()
	    ).then(
	      function (data) {
	          console.log('update of column completed:');
	          //console.dir(data);
	      }
	  );
	} else {
		update(inquiry, updatedFields);
	}

  var old_inquiries = get(inquiries).map(function (i) {
    if ((i.order == inquiry.order) && (i.user_query == inquiry.user_query)){
      return inquiry;
    } else {
      return i;
    }
  });
  inquiries.set(old_inquiries);
}

function convertDateToUTC(date) { return new Date(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate(), date.getUTCHours(), date.getUTCMinutes(), date.getUTCSeconds()); }

function handleQueryChange(e){
    console.log('new query change should be handled!:');
    console.dir(startDateValue);
		loading = true;
    items_.set([]);
    item_ids = {};
    var AdamStartDateValue = new Date();
    if (startDateValue != '') {
      console.dir(startDateValue);
      AdamStartDateValue.setTime(startDateValue.getTime() - (startDateValue.getTimezoneOffset() * 60 * 1000));
    } else {
      AdamStartDateValue = null;
    }
    var AdamEndDateValue = new Date();
    if (endDateValue != '') {
      AdamEndDateValue.setTime(endDateValue.getTime() - (endDateValue.getTimezoneOffset() * 60 * 1000));
    } else {
      AdamEndDateValue = null;
    }
		console.log('query change selected', selectedLocations);
		var selected_ids = selectedLocations.map(function (l) { return l.value; });
		var selected_names = selectedLocations.map(function (l) { return l.label; });
		console.log('query change selected ids', selected_ids);
		var selected = $locations.filter(l => selected_ids.indexOf(l.id) >= 0);
		console.log('query change selected', selected);
		var zero_source_counts = {};
		$sources.forEach(function (s) {
			zero_source_counts[s.short] = 0;
		});
    var updInquiry = {
			name: columnName,
      user_query: query,
      sort: orderField,
      sort_order: orderWay,
      date_start: AdamStartDateValue ? AdamStartDateValue.toISOString() : null,
      date_end: AdamEndDateValue ? AdamEndDateValue.toISOString() : null,
			locations: selected.map(function (l) { return l.id;}),
			read_counts: zero_source_counts
    };
		show_settings = !show_settings;
    updateInquiry(updInquiry);
    console.log('fetchting for query change!');
    fetchFromSources();
}

function fetchFromSources(page, stable_param) {
  var real_page = 0;
  if (typeof(page) !== 'undefined') {
    real_page = page;
  }
  var real_stable = null;
  if (typeof(stable_param) !== 'undefined') {
    real_stable = stable_param;
  }
  if (column_locations.length <= 0) {
    getLocations();
  }

  console.log('should fetch data for colum ' + inquiry.name + ' now!!');
  var selected_sources = []
  $sources.forEach(function (s) {
    if (inquiry['src_' + s.short]) {
      selected_sources.push(s.short);
    } else {
      console.log('Source ' + s.short + ' not fetched because not selected.');
    }
  });
  console.log('fetching ' + selected_sources + ' now ...');

  fetchSource(inquiry.user_query, selected_sources, column_locations, inquiry.date_start, inquiry.date_end, inquiry.sort, inquiry.sort_order, real_stable, real_page, function (fetched_items, original_response) {
    console.log('should set items now!');
    var real_items = get(items_);
    fetched_items.reverse();
    if ((typeof(stable_date) === 'undefined') && (fetched_items.length > 0)) {
      stable_date = fetched_items[0].date;
      console.log('Set stable date for column ' + inquiry.name + 'sorting to: ' + stable_date);
    }
    fetched_items.forEach(function (i) {
      if (typeof(item_ids[i.key]) === 'undefined') {
        real_items.unshift(i);
        item_ids[i.key] = 1;
      }
    });

    var new_source_counts = {};
		var new_per_source_counts = {};
		var total_count = 0;
		var total_new = 0;
    $sources.forEach(function (s) {
      new_source_counts[s.short] = 0;
    });
    original_response.aggregations.source.buckets.forEach(function (b) {
      new_source_counts[b.key] = b.doc_count;
			new_per_source_counts[b.key] = (b.doc_count - inquiry.read_counts[b.key] )|| 0;
			total_new += new_per_source_counts[b.key];
			total_count += b.doc_count;
    });
    console.log('new counts:');
    console.dir(new_source_counts);

		itemsLeft = (real_items.length < total_count);
    items_.set(real_items);
    source_counts.set(new_source_counts);
		inquiry.read_counts = new_source_counts;

		// update column counts here
		if (total_new > 0) {
			console.log('updating read counts in column in db');
			updateInquiry({read_counts: new_source_counts});
		}

    loading = false;
  });

}

function handleSourceButtonClick(src_short) {
  console.log(src_short + 'source selected!');
  items_.set([]);
  item_ids = {};
  var updInquiry = {
  }

  var val = !inquiry['src_' + src_short];
  updInquiry['src_' + src_short] = val;

  updateInquiry(updInquiry);

  loading = true;
  console.log('fetchting for query change!');
  fetchFromSources();
}

// https://ourcodeworld.com/articles/read/713/converting-bytes-to-human-readable-values-kb-mb-gb-tb-pb-eb-zb-yb-with-javascript
function human_readable_numer(numb) {
    if (numb > 0) {
      var base = 1000;
      var i = Math.floor(Math.log(numb) / Math.log(base)),
      sizes = ['', 'K', 'M', 'm', 'B', '', '', '', ''];

      return (numb / Math.pow(base, i)).toFixed(0) * 1 + '' + sizes[i];
    } else {
      return '0';
    }
}


function formatDate(d) {
  let ye = new Intl.DateTimeFormat('en', { year: 'numeric' }).format(d);
  let mo = new Intl.DateTimeFormat('en', { month: 'short' }).format(d);
  let da = new Intl.DateTimeFormat('en', { day: 'numeric' }).format(d);
  return `${da}-${mo}-${ye}`;
}

var interval;


onMount(function () {
  async function fetchData() {
    if (get(fetchingEnabled) && !hidden) {

      fetchFromSources();

      clearInterval(interval);
      interval = setInterval(fetchData, 60000 + (inquiry.order * 1000) + (Math.random() * 2000));
    } else {
      console.log('Fetching not yet enabled for column ' + inquiry.name);
    }
  };
  interval = setInterval(fetchData, 1000 + (Math.random() * 2000));
  fetchData();
});

onDestroy(function () {
  clearInterval(interval);
});

</script>

<svelte:window on:focus={getFocus} on:blur={loseFocus} />

{#if !hidden}
<section class="column-section" out:fade>
<div id="column-{column_id}" class="column">
  <div class="column-title">
    <h2>{ inquiry.name }</h2>
    <IconButton align="end" class="material-icons" aria-label="Instellingen" alt="Instellingen" on:click={() => doSomething()}>tune</IconButton>
  </div>
  {#if show_settings}
  <div class="column-settings" class:active={show_settings} transition:slide="{{ duration: 500 }}">
		<div>
			<Textfield bind:value={columnName} on:change={handleQueryChange} label="Naam" />
		</div>

    <div>
	    <Textfield bind:value={query} on:change={handleQueryChange} label="Zoekopdracht" />
	    <IconButton align="end" class="material-icons" aria-label="Hulp bij een zoekopdracht maken" alt="Hulp bij een zoekopdracht maken" on:click={() => showSearchHelpDialog()}>info</IconButton>
    </div>

		<LocationSelector bind:selectedLocations />

    <div>
    <Select bind:value={orderField} label="Sorteren op">
      <Option value="published" selected={orderField == 'published'}>Datum</Option>
      <Option value="_score" selected={orderField == '_score'}>Relevantie</Option>
    </Select>
    <Select bind:value={orderWay} label="Volgorde">
      <Option value="desc" selected={orderWay == 'desc'}>Aflopend</Option>
      <Option value="asc" selected={orderWay == "asc"}>Oplopend</Option>
    </Select>
    </div>

    <div>
      <Flatpickr options={startDateOptions} bind:value={startDateValue} bind:formattedValue={startDateFormattedValue} on:change={handleStartDateChange} name="start_date" element="#start-picker-{column_id}">
        <div class="flatpickr" id="start-picker-{column_id}">
          <label class="mdc-text-field smui-text-field--standard mdc-ripple-upgraded" style="--mdc-ripple-fg-size:139px; --mdc-ripple-fg-scale:1.7936046986927414; --mdc-ripple-fg-translate-start:-27.5px, -32.5px; --mdc-ripple-fg-translate-end:46.833335876464844px, -41.5px;">
            <input type="text" class="mdc-text-field__input" placeholder="Select Date.." data-input>
            <span class="mdc-floating-label mdc-floating-label--float-above">Startdatum</span>
            <div class="mdc-line-ripple" style="transform-origin: 42px center 0px;"></div>
          </label>
          <IconButton align="end" class="material-icons" aria-label="Datum leegmaken" alt="Datum leegmaken" data-clear>clear</IconButton>
        </div>
      </Flatpickr>
    </div>

    <div>
      <Flatpickr options={endDateOptions} bind:value={endDateValue} bind:formattedValue={endDateFormattedValue} on:change={handleEndDateChange} name="end_date" element="#end-picker-{column_id}">
        <div class="flatpickr" id="end-picker-{column_id}">
          <label class="mdc-text-field smui-text-field--standard mdc-ripple-upgraded" style="--mdc-ripple-fg-size:139px; --mdc-ripple-fg-scale:1.7936046986927414; --mdc-ripple-fg-translate-start:-27.5px, -32.5px; --mdc-ripple-fg-translate-end:46.833335876464844px, -41.5px;">
            <input type="text" class="mdc-text-field__input" placeholder="Select Date.." data-input>
            <span class="mdc-floating-label mdc-floating-label--float-above">Einddatum</span>
            <div class="mdc-line-ripple" style="transform-origin: 42px center 0px;"></div>
          </label>
          <IconButton align="end" class="material-icons" aria-label="Datum leegmaken" alt="Datum leegmaken" data-clear>clear</IconButton>
        </div>
      </Flatpickr>
    </div>

    <div class="column-settings-actions">
      <Button align="begin" variant="unelevated" on:click={() => handleQueryChange()}><Label>Wijzigen</Label></Button>
      <Button align="end" variant="outlined" on:click={() => removeColumn()}><Label>Verwijderen</Label></Button>
    </div>
  </div>
  {/if}
  <div class="column-counts">
    {#each $sources as s}
      <div class="column-counts-source" class:column-counts-source-disabled={!inquiry['src_' + s.short]}>
        <Button on:click={() => handleSourceButtonClick(s.short)}>
          <Label>
            <img src="/images/sources/{ s.short }.svg" alt="{ s.name }" title="{s.name}" class="source-logo"><span title="{$source_counts[s.short] || 0}">{human_readable_numer($source_counts[s.short] || 0)}</span>
          </Label>
        </Button>
      </div>
    {/each}
  </div>
  {#if startDateValue || endDateValue}
  <div class="column-counts column-dates">
    {#if inquiry.date_start && inquiry.date_end}
    {formatDate(startDateValue)} t/m {formatDate(endDateValue)}
    {/if}
    {#if inquiry.date_start && !inquiry.date_end}
    van {formatDate(startDateValue)}
    {/if}
    {#if !inquiry.date_start && inquiry.date_end}
    tot {formatDate(endDateValue)}
    {/if}
  </div>
  {/if}
  <div id="column-contents-{column_id}" class="column-contents">
  {#if !loading && ($items.length <= 0)}
    <p>Er werd nog niks gevonden dat aan je zoekopdracht voldeed.</p>
  {/if}
  {#if show_marker}
    <Fab on:click={doGoToEntry} extended><Label>Nieuwe entries!</Label></Fab>
  {/if}
  {#each $items as entry}
  	<Entry {...entry} column={column_id} entry={entry} />
  {/each}
  {#if !loading && itemsLeft}
  <div id="more-page-link" class="entry entry-paging">
    <Button variant="outlined" on:click={() => doNextPage()}><Label>Meer resultaten</Label></Button>
  </div>
  {/if}
  {#if loading}
    <div class="loading"></div>
  {/if}
  </div>
</div>
</section>
{/if}

<style>
</style>
