<script lang="ts">
  import { onMount } from "svelte";
  import { writable } from "svelte/store";
  import type { PageData } from "./$types";
  import Spinner from "$lib/components/Spinner.svelte";
  let Map: any;
  const infractionsStore = writable();
  export let data: PageData;
  onMount(() => {
    infractionsStore.set(data.unresolvedTf);
    if (typeof window !== "undefined") {
      import("./Map.svelte")
        .then((module) => {
          Map = module.default;
        })
        .catch((error) => {
          console.error("Error importing Map component:", error);
        });
    }
    const eventSource = new EventSource("http://0.0.0.0:5000/sse");
    eventSource.onmessage = (event) => {
      // Handle incoming SSE data
      console.log(event.data);
      infractionsStore.set(event.data);
    };

    eventSource.onerror = (error) => {
      console.error("SSE Error:", error);
      // Handle errors
      eventSource.close();
    };

    
  });
</script>

{#if $infractionsStore !== null}
  {#if Map}
    <Map {infractionsStore} latitude={38.248747} longitude={21.738999} />
  {:else}
    <Spinner />
  {/if}
{:else}
  <Spinner />
{/if}
