<script>
  import "./styles.css";
  import { SvelteToast } from "@zerodevx/svelte-toast";
  import Navigation from "../lib/components/Navigation.svelte";
</script>

<SvelteToast />
<div class="container">
  <!-- Sidebar -->
  <Navigation />
  <!-- Main content area -->
  <div class="content">
    <slot />
  </div>

  
</div>

<footer class="footer">
  <p>&copy; 2022 OnStreetParking. All rights reserved.</p>
</footer>

<style>
  :root {
    --sidebar-width: 250px;
    --sidebar-bg-color: #333;
    --sidebar-text-color: #fff;
    --content-bg-color: #f9f9f9;
    --content-text-color: #333;
    --link-hover-color: #ccc;
    --transition-speed: 0.6s;
  }

  .container {
    display: flex;
    min-height: 100vh;
  }

  .footer {
    background-color: var(--sidebar-bg-color);
    color: var(--sidebar-text-color);
    padding: 20px;
  }

  .content {
    flex: 1;
    background-color: var(--content-bg-color);
    color: var(--content-text-color);
    padding: 20px;
    transition: margin-left var(--transition-speed);
    overflow: auto;
  }

  @media screen and (max-width: 768px) {
    .container {
      flex-direction: column;
    }

    .content {
      margin-top: 20px;
    }
  }
</style>
