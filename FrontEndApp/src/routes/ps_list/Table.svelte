<script lang="ts">
  import { onMount } from "svelte";
  import {
    Table,
    TableBody,
    TableBodyCell,
    TableBodyRow,
    TableHead,
    TableHeadCell,
    Button,
  } from "flowbite-svelte";

  export let ps_store: any;
  let ps_list: any;

  const unsubscribe = ps_store.subscribe((data: any) => {
    ps_list = data;
  });
  function calculateAvg(inp: any, type: number) {
    let jsonInp = JSON.parse(inp);
    let sum = 0.0;
    jsonInp[0].forEach((element: any) => {
      console.log(element);
      sum += Number.parseFloat(element[type]);
    });
    console.log(sum);
    return sum / 4;
  }
  onMount(() => {
    return unsubscribe;
  });
</script>

<Table shadow hoverable={true}>
  <TableHead class="bg-custom-brown text-white overflow-x-auto">
    <TableHeadCell>ID</TableHeadCell>
    <TableHeadCell>Description</TableHeadCell>
    <TableHeadCell>Location</TableHeadCell>
    <TableHeadCell>Number of parking spots</TableHeadCell>
  </TableHead>
  <TableBody>
    {#each ps_list.list as row}
      <TableBodyRow>
        {#each Object.values(row) as cell, index}
          {#if index != 2}
            <TableBodyCell>{cell}</TableBodyCell>
          {:else}
            <TableBodyCell>
              <a
                href={`/map?lat=${calculateAvg(cell, 0)}&lng=${calculateAvg(cell, 1)}`}
                >View {cell}
              </a>
            </TableBodyCell>
          {/if}
        {/each}
      </TableBodyRow>
    {/each}
  </TableBody>
</Table>
