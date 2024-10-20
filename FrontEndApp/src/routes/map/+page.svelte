<script lang="ts">
  import { onMount } from "svelte";
  import { writable } from "svelte/store";
  import type { PageData } from "./$types";
  import Spinner from "$lib/components/Spinner.svelte";
  import { page } from "$app/stores"; // Import the page store from SvelteKit

  let Map: any;
  const infractionsStore = writable();
  export let data: PageData;

  // Extract latitude and longitude from the URL
  let latitude: number;
  let longitude: number;

  $: {
    // Assuming your URL has query parameters like ?lat=...&lng=...
    const urlParams = $page.url.searchParams;
    latitude = parseFloat(urlParams.get("lat")) || 38.248747; // Default latitude if not provided
    longitude = parseFloat(urlParams.get("lng")) || 21.738999; // Default longitude if not provided
  }

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
    <Map {infractionsStore} {latitude} {longitude} />
  {:else}
    <Spinner />
  {/if}
{:else}
  <Spinner />
{/if}
