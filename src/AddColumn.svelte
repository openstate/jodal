<Dialog bind:this={simpleDialog} aria-labelledby="simple-title" aria-describedby="simple-content">
 <!-- Title cannot contain leading whitespace due to mdc-typography-baseline-top() -->
 <Title id="simple-title">Dialog Title</Title>
 <Content id="simple-content">
   Super awesome dialog body text?
 </Content>
 <Actions>
   <Button on:click={() => clicked = 'No'}>
     <Label>No</Label>
   </Button>
   <Button on:click={() => clicked = 'Yes'}>
     <Label>Yes</Label>
   </Button>
 </Actions>
</Dialog>

<script context="module">
  let simpleDialog;

	export function startAddColumn() {
    simpleDialog.open();
	}
</script>

<script>
  import Dialog, {Title, Content, Actions, InitialFocus} from '@smui/dialog';
  import Button, {Label} from '@smui/button';
  import List, {Item, Graphic, Text} from '@smui/list';
  import Radio from '@smui/radio';
  import Slider from '@smui/slider';
  import FormField from '@smui/form-field';

  let clicked = false;
</script>
