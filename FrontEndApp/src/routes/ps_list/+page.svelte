<script lang="ts">
  import Table from "./Table.svelte";
  import Spinner from "../../lib/components/Spinner.svelte";
  import { onMount } from "svelte";
  import { writable } from "svelte/store";
  import type { PageData } from "./$types";

  const ps_store = writable(null);
  export let data: PageData;

  onMount(async () => {
    ps_store.set(data.parkingSites);
  });
</script>

<title>ParkingSite</title>
<header>
  <h1>Parking Sites</h1>
</header>

{#if $ps_store !== null}
  <Table {ps_store} />
{:else}
  <Spinner />
{/if}
