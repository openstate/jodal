<script>
  import { Mastodon, TwitterX, Linkedin, Github, EnvelopeFill } from 'svelte-bootstrap-icons';
  import OSFLogo from '$lib/assets/logo-openstate.png';
  import exampleLogo from '$lib/assets/example-logo.png';
  import { IconHeart } from '@tabler/icons-svelte';
  let input = 'xxx';
</script>

<div class="page">
  <!-- Sidebar -->
  <aside class="navbar navbar-vertical navbar-expand-sm navbar-dark">
    <div class="container-fluid">
      <button class="navbar-toggler" type="button">
        <span class="navbar-toggler-icon"></span>
      </button>
      <h1 class="navbar-brand navbar-brand-autodark">
        <a href="#">
          <img src="{OSFLogo}" width="110" height="32" alt="Tabler" class="navbar-brand-image">
        </a>
      </h1>
      <div class="collapse navbar-collapse" id="sidebar-menu">
        <ul class="navbar-nav pt-lg-3">
          <li class="nav-item">
            <a class="nav-link" href="./">
              <span class="nav-link-title">
                Home
              </span>
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">
              <span class="nav-link-title">
                Link 1
              </span>
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">
              <span class="nav-link-title">
                Link 2
              </span>
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">
              <span class="nav-link-title">
                Link 3
              </span>
            </a>
          </li>
        </ul>
      </div>
    </div>
  </aside>
  <div class="page-wrapper">
    <div class="page-header d-print-none">
      <div class="container-xl">
        <div class="row g-2 align-items-center">
          <div class="col">
            <h2 class="page-title">
              Vertical layout
            </h2>
          </div>
        </div>
      </div>
    </div>
    <div class="page-body">
      <div class="container-xl">
        <div class="row row-deck row-cards">
          <div class="col-sm-6 col-lg-3">
            <div class="card">
              <div class="card-body" style="height: 10rem">
                <a href="#" class="btn" role="button" on:click="{() => input='blaat'}">Update</a>
              </div>
            </div>
          </div>
          <div class="col-sm-6 col-lg-3">
            <div class="card">
              <div class="card-body" style="height: 10rem">{input}</div>
            </div>
          </div>
          <div class="col-sm-6 col-lg-3">
            <div class="card">
              <div class="card-body" style="height: 10rem"></div>
            </div>
          </div>
          <div class="col-sm-6 col-lg-3">
            <div class="card">
              <div class="card-body" style="height: 10rem"></div>
            </div>
          </div>
          <div class="col-lg-6">
            <div class="row row-cards">
              <div class="col-12">
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
          <div class="col-lg-6">
            <div class="card">
              <div class="card-body" style="height: 10rem"></div>
            </div>
          </div>
          <div class="col-12">
            <div class="card">
              <div class="card-body" style="height: 10rem"></div>
            </div>
          </div>
          <div class="col-md-12 col-lg-8">
            <div class="card">
              <div class="card-body" style="height: 10rem"></div>
            </div>
          </div>
          <div class="col-md-6 col-lg-4">
            <div class="card">
              <div class="card-body" style="height: 10rem"></div>
            </div>
          </div>
          <div class="col-md-6 col-lg-4">
            <div class="card">
              <div class="card-body" style="height: 10rem"></div>
            </div>
          </div>
          <div class="col-md-12 col-lg-8">
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
