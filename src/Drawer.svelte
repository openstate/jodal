{#if $drawerOpen}
<section>
    <div class="drawer-container">
      <Drawer variant="modal" bind:this={myDrawer2} bind:open={myDrawer2Open} on:MDCDrawer:closed={() => drawerOpen.update(n => false)}>
        <Content>
          <List>
          <Item href="https://site.bron.live/gids">
            <Text>Gids</Text>
          </Item>

          <Item href="https://site.bron.live/faq">
            <Text>FAQs</Text>
          </Item>
          <Item href="https://site.bron.live/over-bron">
            <Text>Over</Text>
          </Item>
          <div class="social-container">
            <a href="https://github.com/openstate/jodal">
              <img class="social-logo" src="/images/github.svg">
            </a>
            <a href="https://mastodon.social/@bron_live">
              <img class="social-logo" src="/images/mastodon.svg">
            </a>
            <a href="https://twitter.com/bron_live">
              <img class="social-logo" src="/images/twitter.svg">
            </a>
          </div>
          {#if $identity}
            <Item href="//{apiDomainName}/users/simple/logout">
              <Text>Uitloggen</Text>
            </Item>
          {:else}
            {#if !$isTesting}
            <Item href="//www.{domainName}/login/">
              <Text>Inloggen</Text>
            </Item>
            {/if}
          {/if}
          </List>
        </Content>
      </Drawer>

      <Scrim />
    </div>
</section>
{/if}

<script>
  import Drawer, {AppContent, Content, Header, Title, Subtitle, Scrim} from '@smui/drawer';
  import Button, {Label} from '@smui/button';
  import List, {Item, Text, Graphic, Separator, Subheader} from '@smui/list';
  import H6 from '@smui/common/H6.svelte';
  import { drawerOpen, identity, isTesting, apiDomainName, domainName } from './stores.js';

  let clicked = 'nothing yet';
  let myDrawer;
  let myDrawerOpen = false;
  let active = 'Gray Kittens';
  let myDrawer2;
  let myDrawer2Open; // = false;

  let active2 = 'Inbox';

  const unsubscribe = drawerOpen.subscribe(value => {
  		myDrawer2Open = value;
  	});

  function setActive(value) {
    active = value;
    myDrawerOpen = false;
  }

  function setActive2(value) {
    active2 = value;
    drawerOpen.update(n => false);
  }

</script>


<style>
  .drawer-container {
    position: relative;
    display: flex;
    height: 350px;
    max-width: 600px;
  /*  border: 1px solid rgba(0,0,0,.1);*/
    overflow: hidden;
  }

  * :global(.mdc-drawer--modal, .mdc-drawer-scrim) {
    /* This is not needed for a page-wide modal. */
    position: absolute;
  }

  * :global(.app-content) {
    flex: auto;
    overflow: auto;
    position: relative;
    flex-grow: 1;
  }

  .main-content {
    overflow: auto;
    padding: 16px;
    height: 100%;
    box-sizing: border-box;
  }

  .social-logo {
    width: 40px;
    height: 40px;
    flex: 1;
  }

  .social-container {
    display: flex;
  }

  .social-container a {
    display: block;
    flex: 1;
    text-align: center;
  }
</style>
