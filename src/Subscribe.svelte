<Dialog
  bind:open
  bind:this={subscribeDialog}
  aria-labelledby="default-focus-title"
  aria-describedby="default-focus-content"
>
  <Title id="default-focus-title">Abboneer</Title>
  <Content id="default-focus-content">
    <div>
      <Label>zoekopdracht</Label>
      {user_query}
    </div>
    <div>
      <Label>Gemeenten</Label>
      {selected_ids}
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
        <Option value="direct" selected={frequency == 'direct'}>Onmiddelijk</Option>
        <Option value="hourly" selected={frequency == 'hourly'}>Elk uur</Option>
        <Option value="daily" selected={frequency == 'daily'}>Elke dag</Option>
        <Option value="weekly" selected={frequency == 'weekly'}>Elke week</Option>
      </Select>
    </div>
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
  import Textfield, {Input, Textarea} from '@smui/textfield';
  import FloatingLabel from '@smui/floating-label';
  import LineRipple from '@smui/line-ripple';
  import Select, {Option} from '@smui/select';
  import { get } from 'svelte/store';
  import { identity, selected_inquiry, selected_inquiry_id } from './stores.js';

  let open;
  let response = 'Nothing yet.';
  let email = '';
  let frequency = 'direct';
  let user_query = '';
  let selected_ids = [];
  $: if ($identity) { email=$identity.email }
  $: if ($selected_inquiry_id) { user_query = $selected_inquiry[0].user_query; selected_ids = $selected_inquiry[0].locations; }
</script>

<script context="module">
  let subscribeDialog;

	export function showSubscribeDialog(q,i) {
    subscribeDialog.open();
	}
</script>
