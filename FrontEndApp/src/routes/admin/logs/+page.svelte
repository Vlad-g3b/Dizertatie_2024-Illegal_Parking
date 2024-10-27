<script lang="ts">
  import Table from "./Table.svelte";
  import Spinner from "../../../lib/components/Spinner.svelte";
  import { onMount } from "svelte";
  import { writable } from "svelte/store";
  import type { PageData } from "./$types";

  const tf_store = writable(null);
  export let data: PageData;
  export let form: any;
  let message: any = form?.message;

  onMount(async () => {
    tf_store.set(data.logs);
  });
</script>

<title>View Logs</title>
<header>
  <h1>Application Logs</h1>
</header>

{#if $tf_store !== null}
  <Table {tf_store} {message} />
{:else}
  <Spinner />
{/if}
