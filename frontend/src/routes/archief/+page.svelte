<script>
import { onMount } from 'svelte';
import { invalidateAll } from '$app/navigation';
import { identity, apiDomainName } from '$lib/stores';
import { warcCreate, warcStatus, warcDownloadURL } from '$lib/archive';
import { createAsset } from '$lib/asset';

/** @type {import('./$types').PageData} */
export let data;

let url = "";
let heritrix_response = "";
let job_id = "";
let job_timer = null;
let job_status = "";
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
{$identity}
</p>

<label class="form-label">Link</label>  <input type="text" name="url" bind:value={url} on:keydown={handleKeydown} />
<button type="button" class="btn btn-primary"  data-bs-toggle="modal" data-bs-target="#exampleModal" on:click="{handleUrlForm}">
Verstuur
</button>

<div class="table-responsive">
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
        <td><a href="//{$apiDomainName}/archive/warc/download/{a.external_id}" class="btn btn-primary">downloaden</a></td>
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
