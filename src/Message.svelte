<Dialog
  bind:open
  bind:this={msg}
  aria-labelledby="default-focus-title"
  aria-describedby="default-focus-content"
  class="help-dialog"
  on:MDCDialog:closed={() => (close_msg())}
>
  <Title id="default-focus-title">{ title }</Title>
  <Content id="default-focus-content">
  <div class="container">
  { @html content }
  </div>
  </Content>
  <Actions>
    <Button
      default
      use={[InitialFocus]}
      on:click={() => (close_msg())}
    >
      <Label>Sluiten</Label>
    </Button>
  </Actions>
</Dialog>

<script>
import { onMount, onDestroy } from 'svelte';
import { fade } from 'svelte/transition';

import IconButton from '@smui/icon-button';

import Dialog, { Title, Content, Actions, InitialFocus } from '@smui/dialog';
import Button, { Label } from '@smui/button';

import { fetch_feed } from './feed.js';
import { getCookie, setCookie } from './cookies.js';

let showMsg = false;
let open;
let msg;
let title = "";
let content = "";
let link = getCookie('msgLink');
let oldlink = getCookie('msgLink');
let updateTime = 1000;
var interval;
var chk_dialog_interval;

function close_msg() {
  console.log('dialog closed!');
    showMsg = false;
    setCookie('msgLink', link);
}

function check_for_dialog() {
  console.log('check for dialog ' + typeof(msg));
  if (typeof(msg) !== 'undefined') {
    clearInterval(chk_dialog_interval);
    fetch_updates();
    console.log('dialog checked!');
  }
};

function fetch_updates() {
  fetch_feed('https://blog.jodal.nl/category/updates/feed/', function (feed) {
    console.log('got feed items!');
    title = feed.items[0].title;
    link = feed.items[0].link;
    content = feed.items[0].content.replace('<![CDATA[', '').replace(']]>', '');
    showMsg = (oldlink != link);
    if (showMsg) {
      msg.open();
    }
    oldlink = link;
  });
  clearInterval(interval);
  interval = setInterval(fetch_updates, 60000 + (Math.random() * 2000));
}

onMount(function () {
  chk_dialog_interval = setInterval(check_for_dialog, 500);
});

onDestroy(function () {
});

</script>

<style>
</style>
