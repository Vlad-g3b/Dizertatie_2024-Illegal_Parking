<script lang="ts">
  import {page} from "$app/stores"
</script>
<title> HomePage</title>
<nav>
<h1> Smart on StreetParking </h1>

<div class="actions">
  {#if $page.data.session != null}
  Wellcome {$page.data.session.user?.name}
  {/if}
</div>
</nav>