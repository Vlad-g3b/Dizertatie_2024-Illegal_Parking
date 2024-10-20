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

  let tf_list: any;

  const unsubscribe = tf_store.subscribe((data: any) => {
    tf_list = data;
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
      <TableHeadCell>Description</TableHeadCell>
      <TableHeadCell>Location</TableHeadCell>
      <TableHeadCell>Recorded Date</TableHeadCell>
      <TableHeadCell>Resolved Date</TableHeadCell>
      <TableHeadCell>Resolved By</TableHeadCell>
      <TableHeadCell>Status</TableHeadCell>
    </TableHead>
    <TableBody tableBodyClass="divide-y">
      {#each tf_list.TrafficViolationList as tf, index}
        <TableBodyRow>
          <TableBodyCell>{tf.id}</TableBodyCell>
          <TableBodyCell>{tf.description}</TableBodyCell>
          <TableBodyCell>
            <a href="https://www.google.com/maps/place/{tf.location}"> View </a>
          </TableBodyCell>
          <TableBodyCell>{tf.date_ins}</TableBodyCell>
          <TableBodyCell>{tf.date_res}</TableBodyCell>
          <TableBodyCell>{tf.username}</TableBodyCell>
          <TableBodyCell>
            <form method="post" action="?/resolveTf">
              {#if $page.data.session?.user != null}
                {#if tf.resolved == 0}
                  <input type="hidden" name="id" value={tf.id} />
                  <Button pill type="submit">Resolve...</Button>
                  <!-- <button on:click={() => doPost(tf)}> Resolve... </button> -->
                {:else}
                  Resolved
                {/if}
              {/if}
            </form>
          </TableBodyCell>
        </TableBodyRow>
      {/each}
    </TableBody>
  </Table>
</form>
<div id="toast"></div>
