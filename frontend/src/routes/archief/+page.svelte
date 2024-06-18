<script>
import { identity } from '$lib/stores';
import { warcCreate, warcStatus } from '$lib/archive';

let url = "";
let heritrix_response = "";
let job_id = "";

let handleUrlForm = function() {
  //e.preventDefault();
  //alert(url);
  if (url != '') {
    console.log('form submit! : [' + url + ']')
    warcCreate(url).then(function (data) {
      console.log('warc got data', data);
      heritrix_response = data;
      job_id = heritrix_response.job_id;
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
</script>

<h1>Archief</h1>

<p>Hello ,
{$identity}
</p>
  <input type="text" name="url" bind:value={url} on:keydown={handleKeydown} />
<button type="button" class="btn btn-primary"  data-bs-toggle="modal" data-bs-target="#exampleModal" on:click="{handleUrlForm}">
Verstuur
</button>

<div class="modal" id="exampleModal" tabindex="-1">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Modal title</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        {job_id}
      </div>
      <div class="modal-footer">
        <button type="button" class="btn me-auto" data-bs-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary" data-bs-dismiss="modal">Save changes</button>
      </div>
    </div>
  </div>
</div>
