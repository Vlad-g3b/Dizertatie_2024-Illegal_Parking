<script lang="ts">
  import { onMount } from "svelte";
  export let ps_store: any;
  let ps_list: any;

  const unsubscribe = ps_store.subscribe((data: any) => {
    ps_list = data;
  });

  onMount(() => {
    return unsubscribe;
  });
</script>

<table>
  <thead>
    <tr>
      <th>ID</th>
      <th>Description</th>
      <th>Location</th>
      <th>Number of parking spots</th>
    </tr>
  </thead>
  <tbody>
    {#each ps_list.list as row}
      <tr>
        {#each Object.values(row) as cell, index}
          <td>{cell}</td>
        {/each}
      </tr>
    {/each}
  </tbody>
</table>

<style>
  table {
    width: 100%;
    border-collapse: collapse;
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
