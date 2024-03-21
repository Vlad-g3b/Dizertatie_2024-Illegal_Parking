<script lang="ts">
import { onMount } from 'svelte';
import Table from './Table.svelte';
import { writable } from 'svelte/store';

const apiUrl = import.meta.env.VITE_API_URL;
const infractionsStore = writable([]);
  async function getListItems() {
  const res = await fetch(apiUrl + '/getAllTParkingSites');
    if (res.ok) {
        return await res.text();
    } else {
        // Sometimes the API will fail!
        throw new Error('Request failed');
    }
  }

</script>
<title>ParkingSite</title>
<header>
    <h1>Parking Sites</h1>
</header>

{#await getListItems()}
	<p>...waiting</p>
{:then infractionsStore}
  {#if Table}
    <Table {infractionsStore}/>
  {:else}
    <p>Loading...</p>
  {/if}
{:catch error}
	<p style="color: red">{error.message}</p>
{/await}