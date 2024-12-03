<script>
import { onMount } from 'svelte';
import { invalidateAll } from '$app/navigation';
import { identity } from '$lib/stores';
import { warcCreate, warcStatus, warcDownloadURL } from '$lib/archive';
import { createAsset } from '$lib/asset';
import { API_URL } from '$lib/api';


  /**
   * @typedef {Object} Props
   * @property {import('./$types').PageData} data
   */

  /** @type {Props} */
  let { data } = $props();

let url = $state("");
let heritrix_response = "";
let job_id = $state("");
let job_timer = null;
let job_status = $state("");
let job_running = false;

let handleUrlForm = function() {
  //e.preventDefault();
  //alert(url);
  if (url != '') {
    console.log('form submit! : [' + url + ']')
    warcCreate(url).then(function (data) {
      console.log('warc got data', data);
      heritrix_response = data;
      job_id = heritrix_response.job_id;
      createAsset(url, job_id);
      initiateStatusUpdates();
      invalidateAll();
    });
  } else {
    console.log('no url specified');
  }
};

function handleKeydown(e) {
  if (e.key == 'Enter') {
    console.log('enter pressed');
    handleUrlForm();
  }
}

function getStatusUpdate() {
  console.log('warc getting status update');
  warcStatus(job_id).then(function (data) {
    console.log('warc status data:', data);
    heritrix_response = data;
    job_status = data.job.crawlExitStatus;
    job_running = data.job.isRunning;
    if (job_status == "FINISHED") {
      clearInterval(job_timer);
      invalidateAll();
    }
  });
}

function initiateStatusUpdates() {
  console.log('warc initiatin status updates');
  job_timer = setInterval(function () {
    getStatusUpdate();
  }, 1000);
}

onMount(() => {
		const interval = setInterval(() => {
			invalidateAll();
		}, 30000);

		return () => {
			clearInterval(interval);
		};
	});
</script>

<h1>Archief</h1>

<p>Hello ,
{#if $identity}
{$identity.given_name}
{:else}
anonymous
{/if}
</p>

<label class="form-label">Link</label>  <input type="text" name="url" bind:value={url} onkeydown={handleKeydown} />
<button type="button" class="btn btn-primary" onclick={handleUrlForm}>
Verstuur
</button>

<div class="table-responsive table-heritrix">
  <table class="table table-vcenter">
    <thead>
      <tr>
        <th>URL</th>
        <th>Acties</th>
      </tr>
    </thead>
    <tbody>

    {#each data.assets as a}
      <tr>
        <td><a href="{a.url}" target="_blank">{a.url}</a></td>
        {#if (typeof(a.status) !== 'undefined') && (typeof(a.status.job) !== 'undefined') && (a.status.job.isRunning == 'false')}
        <td><a href="{API_URL}/archive/warc/download/{a.external_id}" class="btn btn-primary">downloaden</a></td>
        {:else}
        <td class="text-secondary"><span class="status status-azure">bezig...</span></td>
        {/if}
      </tr>
    {/each}

    </tbody>
  </table>
</div>

<div class="modal" id="exampleModal" tabindex="-1">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Status</h5>
      </div>
      <div class="modal-body">
      {#if job_status != "FINISHED"}
        <p>Het WARC bestand wordt gegenereerd, even geduld aub.</p>
      {/if}
      {#if job_status == "FINISHED"}
        <p>Het bestand is gegenereerd. Klink op de onderstaande knop om het te downloaden.</p>
        <a href="{warcDownloadURL(job_id)}" class="btn btn-primary">Downloaden</a>
      {/if}
      </div>
      <div class="modal-footer">
        <button type="button" class="btn me-auto" data-bs-dismiss="modal">Sluiten</button>
      </div>
    </div>
  </div>
</div>
