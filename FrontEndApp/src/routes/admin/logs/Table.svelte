<script lang="ts">
  import { mount, onMount } from "svelte";
  import { Button } from "flowbite-svelte";
  import { page } from "$app/stores";
  import Toast from "../../../lib/components/Toast.svelte";

  import {
    Table,
    TableBody,
    TableBodyCell,
    TableBodyRow,
    TableHead,
    TableHeadCell,
    Checkbox,
  } from "flowbite-svelte";

  export let tf_store: any;
  export let message: any;

  let logs: any;

  const unsubscribe = tf_store.subscribe((data: any) => {
    logs = data;
  });
  onMount(() => {
    if (message != null) {
      let mountPoint: any = document.getElementById("toast");

      mount(Toast, { target: mountPoint, props: { message } });
    }

    return unsubscribe;
  });
</script>

<form method="POST">
  <Table shadow hoverable={true}>
    <TableHead class="bg-custom-brown text-white overflow-x-auto">
      <TableHeadCell>ID</TableHeadCell>
      <TableHeadCell>Operation Type</TableHeadCell>
      <TableHeadCell>Operation Level</TableHeadCell>
      <TableHeadCell>Username</TableHeadCell>
      <TableHeadCell>Description</TableHeadCell>
      <TableHeadCell>Date</TableHeadCell>
    </TableHead>
    <TableBody tableBodyClass="divide-y">
      {#each logs as lg, index}
        <TableBodyRow>
          <TableBodyCell>{lg.lg_id}</TableBodyCell>
          <TableBodyCell>{lg.op_type}</TableBodyCell>
          <TableBodyCell>{lg.op_level}</TableBodyCell>
          <TableBodyCell>{lg.usr_name}</TableBodyCell>
          <TableBodyCell>{lg.lg_description}</TableBodyCell>
          <TableBodyCell>{lg.lg_date_ins}</TableBodyCell>
        </TableBodyRow>
      {/each}
    </TableBody>
  </Table>
</form>
<div id="toast"></div>
