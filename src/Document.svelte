<Dialog
  id="dialog-doc"
  bind:open
  bind:this={docDialog}
  on:MDCDialog:opened={() => scrollHighlightIntoView()}
  aria-labelledby="default-focus-title"
  aria-describedby="default-focus-content"
  class="document-dialog"
>
  <Title id="default-focus-title">{$item.title}</Title>
  <Content id="default-focus-content">
    <div class="document-dialog-content-tools">
      <h4>Exporteren</h4>
      {#if $item.source == 'openspending' && (typeof($item.data) !== 'undefined') && (typeof($item.data.label) !== 'undefined')}
        {#if typeof($GoogleSpreadSheetId) === 'undefined'}
          {#if converting}
            <Label>Converteren ...</Label>
          {:else}
            <GoogleAuth text="Exporteer" clientId="{googleClientId}" on:auth-success={(e) => handleGoogleSignin(e)} />
          {/if}
        {:else}
          <a href="https://docs.google.com/spreadsheets/d/{$GoogleSpreadSheetId}/edit" target="_blank" class="mdc-button document-download-button">
            <Label>Openen</Label>
          </a>
        {/if}
        <h4>Downloaden als:</h4>
        {#each export_formats[$item.source] as fmt}
          <a href="//{apiDomainName}/documents/download/{$item.source}/{$item.data.label.document_id}?format={fmt}" target="_blank" class="mdc-button document-download-button">
            <Label>{fmt}</Label>
          </a>
        {/each}
      {:else}
      { @html $description }
      {/if}

      {#if ($item.source == 'poliflw' || $item.source == 'openbesluitvorming' || $item.source == 'cvdr') && (typeof($item._id) !== 'undefined')}
        <h4>Downloaden als:</h4>
        {#each export_formats[$item.source] as fmt}
          <a href="//{apiDomainName}/documents/download/{$item.source}/{$item._id}?format={fmt}" target="_blank" class="mdc-button document-download-button">
            <Label>{fmt}</Label>
          </a>
        {/each}
      {/if}

    </div>
    <div class="document-dialog-content-description">
      { @html $item.highlighted_description }
    </div>
  </Content>
  <Actions>
    {#if $item.doc_url}
    <a href="{$item.doc_url}" target="_blank" class="mdc-button">
      <Label>Ga naar bron</Label>
    </a>
    {:else}
    <a href="{$item.url}" target="_blank" class="mdc-button">
      <Label>Ga naar bron</Label>
    </a>
    {/if}

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

  import GoogleAuth from './GoogleAuth.svelte';
  import Dialog, { Title, Content, Actions, InitialFocus } from '@smui/dialog';
  import Button, { Group, GroupItem, Label, Icon } from '@smui/button';
  import { writable, get, derived } from 'svelte/store';
  import { identity, apiDomainName, fetchDocument } from './stores.js';
  let converting = false;
  let open;
  let response = 'Nothing yet.';
  let export_formats = {
    'openspending': ['csv', 'json'],
    'poliflw': ['txt', 'json'],
    'openbesluitvorming': ['txt', 'json'],
    'cvdr': ['txt', 'json']
  };

  const googleClientId = runEnvironment.env.googleClientId;

  function scrollHighlightIntoView() {
    var highlight_em = document.getElementsByClassName('document-dialog-content-description')[0].getElementsByTagName('em');
    console.log(highlight_em);
    if (highlight_em.length > 0) {
      console.log('SCROLL INTO VIEW');
      highlight_em[0].scrollIntoView();
      highlight_em[0].scrollBy(0, -60); // small correction bc somethings thing is not shown
    }
  }

  async function getOpenspendingData() {
    console.log('getting spreadsheet data:')
    var url = "//" + apiDomainName + "/documents/download/" + $item.source + '/' + $item.data.openspending_document_id + '?format=json';
    return fetch(url)
      .then(r => r.json())
      .then(data => {
        console.log('got spreadsheet data:');
        console.log(data);
        return data;
      });
  };

  function appendValues(spreadsheetId, range, valueInputOption, _values, callback) {
    // [START sheets_append_values]
    var values = [
      [
        // Cell values ...
      ],
      // Additional rows ...
    ];
    // [START_EXCLUDE silent]
    values = _values;
    // [END_EXCLUDE]
    var body = {
      values: values
    };
    gapi.client.sheets.spreadsheets.values.append({
       spreadsheetId: spreadsheetId,
       range: range,
       valueInputOption: valueInputOption,
       resource: body
    }).then((response) => {
      var result = response.result;
      console.log(`${result.updates.updatedCells} cells appended.`)
      // [START_EXCLUDE silent]
      callback(response);
      // [END_EXCLUDE]
    });
    // [END sheets_append_values]
  }

  function handleGoogleSignin(e) {
        console.log('Google signin worked!');
        console.dir(e.detail.user);
        converting = true;
        var data_promise = getOpenspendingData();
        var auth = gapi.auth2.getAuthInstance();
        gapi.load("client", async function() {
          console.log('gapi.client loaded!');
          gapi.client.load("sheets", "v4", async function() {
            console.log('gapi sheets loaded!');
            var spreadsheet_promise = gapi.client.sheets.spreadsheets.create({
              properties: {
                title: $item.location + ' - ' + $item.title
              }
            }).then((response) => {
              console.log('spreadsheet created:', response);
              return response;
            });
            Promise.all([data_promise, spreadsheet_promise]).then(function (values) {
              console.log('all promises deliviered:');
              console.dir(values);
              if (values.length == 2) {
                var data_keys = Object.keys(values[0][0]);
                var data = values[0].map(function (r) {
                  return data_keys.map(function (k) { return r[k];});
                });
                data.splice(0, 0, data_keys);  // add header information
                console.log('Converted csv data');
                console.dir(data);
                var sheet = values[1];
                var sheetName = sheet.result.sheets[0].properties.title;
                appendValues(sheet.result.spreadsheetId, sheetName + "!A:A", "USER_ENTERED", data, function (r) {
                  console.log('appended!');
                  console.dir(r);
                  // TODO: constructy link to edit document and show
                  GoogleSpreadSheetId.set(sheet.result.spreadsheetId);
                  converting = false;
                });
              }
            });
          });
        });
        // });
  };
</script>

<script context="module">
  let docDialog;
  let item = writable({});
  let description = writable("");
  let GoogleSpreadSheetId = writable(undefined);

  function getDocumentTools() {
    var url = 'https://blog.jodal.nl/?page_id=14&content-only=1';
    return fetch(
      url, {cache: 'no-cache'})
        .then(res => {
            return res.text();
        }).then(
          function (data) {
            console.log('got document data:');
            console.dir(data);
            description.set(data);
          }
      );
  }

  function _showDocumentDialog(doc) {
    if (typeof(doc.highlight) !== 'undefined') {
      var highlight_tags_removed = doc.highlight.replace('<em>', '').replace('</em>', '');
      if (typeof(doc.description) !== 'undefined') {
        doc.highlighted_description = doc.description.replaceAll(highlight_tags_removed, doc.highlight);
      } else {
        doc.highlighted_description = doc.highlight;
      }
    } else {
      doc.highlighted_description = doc.description;
    }
    item.set(doc);
    GoogleSpreadSheetId.set(undefined);
    getDocumentTools();
    docDialog.open();
  }

	export function showDocumentDialog(doc) {
    var doc_id = doc._id;
    var doc_highlight = doc.highlight;

    if(typeof(doc.description) === 'undefined') {
      console.log('Show document: Getting data for document', doc);
      fetchDocument(doc_id).then(function(data) {
        console.log('Show document: got document data:', data);
        if (data.hits.total.value > 0) {
          doc = data.hits.hits[0]._source;
        }
        doc.highlight = doc_highlight;
        _showDocumentDialog(doc)
      });
    } else {
      _showDocumentDialog(doc);
    }
	}
</script>
