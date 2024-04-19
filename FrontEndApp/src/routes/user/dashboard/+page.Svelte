<script lang="ts">
  import { page } from "$app/stores";
</script>

<title> HomePage User</title>
<nav>
  <h1>Dashboard</h1>

  <div>
    {#if $page.data.session != null}
      Welcome {$page.data.session.user?.name}
    {/if}
  </div>
</nav>
