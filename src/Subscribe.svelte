<Dialog
  bind:open
  bind:this={subscribeDialog}
  aria-labelledby="default-focus-title"
  aria-describedby="default-focus-content"
>
  <Title id="default-focus-title">Abboneer</Title>
  <Content id="default-focus-content">
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
  import { identity } from './stores.js';

  let open;
  let response = 'Nothing yet.';
  let email = '';
  let frequency = 'direct';

  $: if ($identity) { email=$identity.email }
</script>

<script context="module">
  let subscribeDialog;

	export function showSubscribeDialog() {
    subscribeDialog.open();
	}
</script>
