<script lang="ts">
  import Table from "./Table.svelte";
  import Spinner from "../../lib/components/Spinner.svelte";
  import { onMount } from "svelte";
  import { writable } from "svelte/store";
  import type { PageData } from "./$types";

  const tf_store = writable(null);
  export let data: PageData;

  onMount(async () => {
    tf_store.set(data.trafficViolations);
    console.log("call onMount?");
  });
</script>

<title>TrafficViolation</title>
<header>
  <h1>Manage TrafficViolation</h1>
</header>

{#if $tf_store !== null}
  <Table {tf_store} />
{:else}
  <Spinner />
{/if}
