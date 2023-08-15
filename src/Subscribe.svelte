<Dialog
  bind:open
  bind:this={subscribeDialog}
  aria-labelledby="default-focus-title"
  aria-describedby="default-focus-content"
>
  <Title id="default-focus-title">Abboneer</Title>
  <Content id="default-focus-content">
  <div>
    <Label>beschrijving</Label>
    {description}
  </div>
    <div>
      <Label>zoekopdracht</Label>
      {user_query}
    </div>
    <div>
      <Label>Gemeenten</Label>
      {selected_ids}
    </div>
    <div>
      <Label>Bronnen</Label>
      {ood_sources}
    </div>
    <div>
      <Label>E-mail</Label>
      <Textfield>
        <Input bind:value={email} id="subscribe-email" />
      </Textfield>
    </div>
    <div>
      <Label>Frequentie</Label>
      <Select bind:value={frequency}>
        <Option value="" selected={frequency == ''}>Onmiddelijk</Option>
        <Option value="hourly" selected={frequency == '1h'}>Elk uur</Option>
        <Option value="daily" selected={frequency == '24h'}>Elke dag</Option>
        <Option value="weekly" selected={frequency == '168h'}>Elke week</Option>
      </Select>
    </div>
  </Content>
  <Actions>
  <Button
    default
    use={[InitialFocus]}
    on:click={() => (subscriptionNew(user_query, selected_ids, ood_sources, description, email, frequency))}
  >
    <Label>Abboneer</Label>
  </Button>
    <Button
      on:click={() => (response = 'It will be glorious.')}
    >
      <Label>Annuleer</Label>
    </Button>
  </Actions>
</Dialog>

<script>
  import Dialog, { Title, Content, Actions, InitialFocus } from '@smui/dialog';
  import Button, { Label } from '@smui/button';
  import Textfield, {Input, Textarea} from '@smui/textfield';
  import FloatingLabel from '@smui/floating-label';
  import LineRipple from '@smui/line-ripple';
  import Select, {Option} from '@smui/select';
  import { get } from 'svelte/store';
  import { identity, selected_inquiry, selected_inquiry_id, sources } from './stores.js';
  import {subscriptionNew } from './binoas.js';

  let open;
  let response = 'Nothing yet.';
  let email = '';
  let frequency = 'direct';
  let user_query = '';
  let selected_ids = [];
  let ood_sources = [];
  let description = '';
  $: if ($identity) { email=$identity.email }
  $: if ($selected_inquiry_id) {description = $selected_inquiry[0].name; user_query = $selected_inquiry[0].user_query; selected_ids = $selected_inquiry[0].locations; ood_sources = $sources.map((l) => l.short).filter((l) => $selected_inquiry[0]['src_' + l]) }
</script>

<script context="module">
  let subscribeDialog;

	export function showSubscribeDialog(q,i) {
    subscribeDialog.open();
	}
</script>
