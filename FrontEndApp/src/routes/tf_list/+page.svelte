<script lang="ts">
  import Table from "./Table.svelte";
  import Spinner from "../components/Spinner.svelte";
  import { onMount } from "svelte";
  const apiUrl = import.meta.env.VITE_API_URL;
  let tf_list: any;
  onMount(async () => {
    tf_list = await getAllTrafficViolation();
});
  async function getAllTrafficViolation() {
    const res = await fetch(apiUrl + "/getAllTrafficViolation");
    if (res.ok) {
      const data = await res.json();
      return data;
    } else {
      // Sometimes the API will fail!
      throw new Error("Request failed");
    }
  }
</script>

<title>TrafficViolation</title>
<header>
  <h1>Manage TrafficViolation</h1>
</header>

{#await getAllTrafficViolation()}
  <p>Loading ...</p>
  <Spinner />
{:then tf_list}
    <Table {tf_list} />
  {/await}
