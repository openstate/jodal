<script>
import BronLogo from '$lib/assets/bron-logo.svg';
import MastodonLogo from '$lib/assets/mastodon.svg';
import TwitterLogo from '$lib/assets/twitter.svg';
import GitHubLogo from '$lib/assets/github.svg';

</script>
<nav class="navbar navbar-expand-lg bg-body-tertiary">
  <div class="container-fluid">
    <a class="navbar-brand" href="/">
      <img src="{BronLogo}">
    </a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="d-flex brand-byline">
    alle overheidsdata — monitor, filter, stuur door.
    </div>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <a class="nav-link" href="https://site.bron.live/gids" target="_blank">Gids</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="https://site.bron.live/faq" target="_blank">FAQs</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="https://site.bron.live/over-bron" target="_blank">Over</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="https://github.com/openstate/jodal"  target="_blank">
            <img src="{GitHubLogo}" alt="Github" class="social-logo" />
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="https://mastodon.social/@bron_live"  target="_blank">
            <img src="{MastodonLogo}" alt="Mastodon" class="social-logo" />
          </a>
        </li>
        <li class="nav-item ms-auto">
          <a class="nav-link" href="https://twitter.com/bron_live"  target="_blank">
            <img src="{TwitterLogo}" alt="Twitter" class="social-logo" />
          </a>
        </li>
      </ul>
    </div>
  </div>
</nav>

<style>
.navbar {
  height: 85px;
}

.navbar-brand img {
  width: 190px;
  height: 42px;
}

.nav-link {
	color: #5E5E5E;
	font-weight: 600;
	font-size: 16px;
	font-style: normal;
	line-height: normal;
	margin: 30px;
	text-decoration: none;
}

.social-logo {
  width: 20px;
  height: 20px;
}

.brand-byline {
	font-size: 17px;
	line-height: 48px;
	font-weight: 400;
	color: #767676;
	margin-left: 30px;
	text-align: left;
}
</style>
