<script lang="ts">
  import Chart from "../../lib/components/Chart.svelte";
  import { writable } from "svelte/store";
  import type { PageData } from "./$types";
  import { onMount } from "svelte";
  import Spinner from "$lib/components/Spinner.svelte";
  const infractionsStore = writable(null);
  export let data: PageData;

  onMount(async () => {
    infractionsStore.set(data.stats);
  });
</script>

<title>Statistics</title>
<header>
  <h1>Statistics</h1>
</header>

{#if $infractionsStore !== null}
  <Chart {infractionsStore} />
{:else}
  <Spinner />
{/if}
