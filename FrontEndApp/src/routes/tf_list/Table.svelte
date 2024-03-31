<script lang="ts">
  import { writable } from "svelte/store";
  //export let infractionsStore: import("svelte/store").Writable<Array<object>>;
  export let tf_list: any;
  const response = writable();
  async function doPost(tf: any) {
    const apiUrl = import.meta.env.VITE_API_URL;
    let data: { tf_id: any; tf_type: string; is_resolved: number } = {
      tf_id: tf.id,
      tf_type: "TrafficViolation",
      is_resolved: 1,
    };
    const res = await fetch(apiUrl + "/updateResolved", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    const json = await res.json();
    response.set(data);
  }
</script>

{#if $response}
  <p>Response from server: {$response} {console.log({ $response })}</p>
{/if}
<table>
  <thead>
    <tr>
      <th>ID</th>
      <th>Description</th>
      <th>Location</th>
      <th>Recorded Date</th>
      <th>Resolved Date</th>
      <th>Status</th>
    </tr>
  </thead>
  <tbody>
    {#each tf_list.TrafficViolationList as tf}
      <tr>
        <td>{tf.id}</td>
        <td>{tf.description}</td>
        <td>{tf.location}</td>
        <td>{tf.date_ins}</td>
        <td>{tf.date_res}</td>
        <td>
          {#if tf.resolved == 0}
            <button on:click={() => doPost(tf)}> Resolve... </button>
          {:else}
            Resolved
          {/if}
        </td>
      </tr>
    {/each}
  </tbody>
</table>

<style>
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 10px;
  }

  th,
  td {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 8px;
  }

  th {
    background-color: #f2f2f2;
  }

  tr:nth-child(even) {
    background-color: #f2f2f2;
  }
</style>
