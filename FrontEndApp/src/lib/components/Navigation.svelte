<script>
  import "../../routes/styles.css";
  import { page } from "$app/stores";
  import { signIn, signOut } from "@auth/sveltekit/client";
</script>

<div class="sidebar">
  <!-- HTML !-->
  <div class="container-box">
    {#if $page.data.session != null}
      <div class="box">
        <img
          class="rounded-image"
          alt="profile-pic"
          src={$page.data.session.user?.image}
        />
      </div>
      <div class="box">
        <div class="box text-column">
          Welcome {$page.data.session.user?.name}
        </div>
        <div class="container-box">
          <button
            class="button-24"
            on:click={() => signOut({ callbackUrl: $page.url.origin })}
            >Sign Out</button
          >
        </div>
      </div>
    {:else}
      <div class="box">
        <button class="button-24" on:click={() => signIn("github")}
          >Sign In
        </button>
      </div>
    {/if}
  </div>
  <h2>Navigation</h2>
  <ul>
    <li><a href="/map">Live map</a></li>
    <li><a href="/live_feed">Live Feed</a></li>
    <li><a href="/tf_list">Traffic Violations</a></li>
    <li><a href="/ps_list">Parking Sites</a></li>
    <li><a href="/statistics">Statistics</a></li>
  </ul>
</div>

<style>
  .container-box {
    display: flex;
    overflow: hidden;
    padding: 10px;
    justify-content: center;
    align-items: center;
    text-align: center;
  }

  .box {
    flex: 1; /* To distribute space equally */
  }

  .sidebar {
    width: var(--sidebar-width);
    background-color: var(--sidebar-bg-color);
    color: var(--sidebar-text-color);
    padding: 20px;
  }

  .sidebar h2 {
    margin-bottom: 20px;
  }

  .sidebar ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  .sidebar li {
    margin-bottom: 10px;
  }

  .sidebar a {
    display: block;
    padding: 10px;
    color: inherit;
    text-decoration: none;
    transition: color var(--transition-speed);
  }

  .sidebar a:hover {
    background-color: var(--link-hover-color);
  }
  .rounded-image {
    max-width: 80%; /* Ensures the image doesn't exceed the width of its container */
    max-height: 80%; /* Ensures the image doesn't exceed the height of its container */
    width: auto; /* Allows the image to scale proportionally */
    height: auto; /* Allows the image to scale proportionally */
    border-radius: 50%; /* Makes the image round */
    overflow: hidden; /* Ensures the border-radius is applied correctly */
  }

  @media screen and (max-width: 768px) {
    .sidebar {
      width: 100%;
      text-align: center;
    }
  }
</style>
