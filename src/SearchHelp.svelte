<Dialog
  bind:open
  bind:this={searchHelpDialog}
  aria-labelledby="default-focus-title"
  aria-describedby="default-focus-content"
>
  <Title id="default-focus-title">Help bij zoekopdracht</Title>
  <Content id="default-focus-content">
  <table class="table table-striped table-condensed table-responsive ng-scope">
    <thead>
    <tr>
      <th>Zoekopdracht</th>
      <th style="white-space: nowrap;">Vind documenten die…
      </th><th>
    </th></tr>
    </thead>
    <tbody>
    <tr>
      <td>vvd windmolens</td>
      <td>het woord "vvd" of "windmolens" bevatten</td>
    </tr>
    <tr>
      <td>vvd + windmolens</td>
      <td>zowel het woord "vvd" en "windmolens" bevatten</td>
    </tr>
    <tr>
      <td>vvd | windmolens</td>
      <td>minstens een van de woorden "vvd" of "windmolens" bevatten</td>
    </tr>
    <tr>
      <td>vvd -windmolens</td>
      <td>het woord "vvd" bevatten, maar <em>niet</em> "windmolens"</td>
    </tr>
    <tr>
      <td>"vvd windmolens"</td>
      <td>die de woorden "vvd" en "windmolens" in deze exacte volgorde bevatten</td>
    </tr>
    <tr>
      <td>euro*</td>
      <td>die woorden bevatten die beginnen met "euro" (euro, Europa, Europees kampioenschap)</td>
    </tr>
    <tr>
      <td>(vvd windmolens) | euro*</td>
      <td>die "vvd" <em>en</em> "windmolens" bevatten, <em>of</em> woorden die beginnen met "euro" (haakjes geven prioriteit
        aan)
      </td>
    </tr>
    </tbody>
  </table>
  </Content>
  <Actions>
    <Button
      default
      use={[InitialFocus]}
      on:click={() => (response = 'It will be glorious.')}
    >
      <Label>Sluiten</Label>
    </Button>
  </Actions>
</Dialog>

<script>
  import Dialog, { Title, Content, Actions, InitialFocus } from '@smui/dialog';
  import Button, { Label } from '@smui/button';

  let open;
  let response = 'Nothing yet.';
</script>

<script context="module">
  let searchHelpDialog;

	export function showSearchHelpDialog() {
    searchHelpDialog.open();
	}
</script>
