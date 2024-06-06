<script>
let url = "";

let handleUrlForm = function() {
  //e.preventDefault();
  //alert(url);
  console.log('form submit! : [' + url + ']')
};

function handleKeydown(e) {
  if (e.key == 'Enter') {
    console.log('enter pressed');
    handleUrlForm();
  }
}
</script>

<h1>Archief</h1>

  <input type="text" name="url" bind:value={url} on:keydown={handleKeydown} />
<button type="button" class="btn btnrimary" on:click="{handleUrlForm}">
Verstuur
</button>
<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
  Launch demo modal
</button>

<div class="modal" id="exampleModal" tabindex="-1">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Modal title</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        Lorem ipsum dolor sit amet, consectetur adipisicing elit. Adipisci animi beatae delectus deleniti dolorem eveniet facere fuga iste nemo nesciunt nihil odio perspiciatis, quia quis reprehenderit sit tempora totam unde.
      </div>
      <div class="modal-footer">
        <button type="button" class="btn me-auto" data-bs-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary" data-bs-dismiss="modal">Save changes</button>
      </div>
    </div>
  </div>
</div>
