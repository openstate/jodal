<script>
  import { Mastodon, TwitterX, Linkedin, Github, EnvelopeFill } from 'svelte-bootstrap-icons';
  import OSFLogo from '$lib/assets/logo-openstate.png';
  import exampleLogo from '$lib/assets/example-logo.png';
</script>

<div class="page">
  <header class="navbar navbar-expand-sm navbar-light d-print-none">
    <div class="container-xl">
      <h1 class="navbar-brand navbar-brand-autodark d-none-navbar-horizontal pe-0 pe-md-3">
        <a href="#">
          <img src="{OSFLogo}" width="110" height="32" alt="Tabler" class="navbar-brand-image" />
        </a>
      </h1>

      <div class="navbar-nav flex-row order-md-last">
        <div class="nav-item">
          <a href="#" class="nav-link d-flex lh-1 text-reset p-0">
            <span class="avatar avatar-sm" style="background-image: url(...)"></span>
            <div class="d-none d-xl-block ps-2">
              <div>Paweł Kuna</div>
              <div class="mt-1 small text-secondary">UI Designer</div>
            </div>
          </a>
        </div>
      </div>
    </div>
  </header>


  <div class="page-wrapper">
    <div class="page-body">
      <div class="container-xl">
        <div class="row row-deck row-cards">
          <div class="col-4">
            <div class="card">
              <div class="card-body" style="height: 10rem">

              <div class="dropdown">
                <button type="button" class="btn dropdown-toggle" data-bs-toggle="dropdown">
                  <!-- SVG icon from http://tabler-icons.io/i/calendar -->
                  <svg>...</svg>
                </button>
                <div class="dropdown-menu">
                  <a class="dropdown-item" href="#">
                    Action
                  </a>
                  <a class="dropdown-item" href="#">
                    Another action
                  </a>
                </div>
              </div>

              </div>
            </div>
          </div>
          <div class="col-4">
            <div class="card">
              <div class="card-body" style="height: 10rem"></div>
            </div>
          </div>
          <div class="col-4">
            <div class="card">
              <div class="card-body" style="height: 10rem"></div>
            </div>
          </div>
          <div class="col-12">
            <div class="card">
              <div class="card-body" style="height: 10rem"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
