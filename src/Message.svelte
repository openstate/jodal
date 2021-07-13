{#if showMsg}
<div class="message" bind:this={msg} in:fade out:fade>
<span>{ title } <a href="{ link }" target="_blank">Meer &gt;</a></span>
<IconButton class="material-icons close-btn" aria-label="Sluiten" on:click={() => close_msg() } title="Sluiten">close</IconButton>
</div>
{/if}

<script>
import { onMount, onDestroy } from 'svelte';
import { fade } from 'svelte/transition';

import IconButton from '@smui/icon-button';

import { fetch_feed } from './feed.js';
import { getCookie, setCookie } from './cookies.js';

let showMsg = false;
let msg;
let title = "";
let link = getCookie('msgLink');
let oldlink = getCookie('msgLink');
var interval;

function close_msg() {
    showMsg = false;
    setCookie('msgLink', link);
}

function fetch_updates() {
  fetch_feed('https://blog.jodal.nl/category/updates/feed/', function (feed) {
    console.log('got feed items!');
    title = feed.items[0].title;
    link = feed.items[0].link;
    showMsg = (oldlink != link);
    oldlink = link;
  });
  clearInterval(interval);
  interval = setInterval(fetch_updates, 60000 + (Math.random() * 2000));
}

onMount(function () {
  fetch_updates();
});

onDestroy(function () {
});

</script>

<style>
</style>
