<script>
  import logo_openstate_wit from '$lib/assets/logo-openstate-wit.png';
</script>

<section class="topbar d-flex flex-row justify-content-start fixed-top">
  <div class="row d-flex container-fluid align-items-center">
    <div class="col-md-6 d-flex align-items-center">
      <img src="{logo_openstate_wit}" alt="Logo Open State Foundation" width="100"/>
      <div class="line"></div>
      <a href="https://openstate.eu/nl/doneren/" class="btn button-help-mee">Help mee</a>
    </div>
  </div>
</section>
<div class="topbar-scroll-opaque d-flex flex-row fixed-top">
</div>

<style>
  .topbar-scroll-opaque {
    margin-top: 40px;
    height:20px;
    background-color: var(--white);
    opacity: 0.8;
  }

  .topbar {
      background-color: var(--petrol);
      height: 40px;
  }

  .line {
      width: 2px;
      height: 30px;
      background-color: var(--white);
      margin-left: 15px;
      margin-right: 15px;
  }

  .button-help-mee {
      background-color: var(--white);
      color: var(--primary-color);
      margin: 2px;
      padding: 2px 5px 2px 5px;
      font-size: 12px;
      border-radius: var(--border-radius);
      font-weight: 500;
  }
</style>
