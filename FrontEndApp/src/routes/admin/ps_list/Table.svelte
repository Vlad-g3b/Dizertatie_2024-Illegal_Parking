<script lang="ts">
  import { mount, unmount, onMount } from "svelte";
  import {
    Table,
    TableBody,
    TableBodyCell,
    TableBodyRow,
    TableHead,
    TableHeadCell,
    Button,
    Checkbox,
    Input,
    Label,
    Modal,
  } from "flowbite-svelte";
  import Toast from "../../../lib/components/Toast.svelte";

  export let ps_store: any;

  export let message: any;
  let ps_list: any;
  let formModal = false;
  let itemToEdit: any;
  const unsubscribe = ps_store.subscribe((data: any) => {
    ps_list = data;
  });

  function calculateAvg(inp: any, type: number) {
    let jsonInp = JSON.parse(inp);
    let sum = 0.0;
    jsonInp[0].forEach((element: any) => {
      sum += Number.parseFloat(element[type]);
    });
    return sum / 4;
  }
  onMount(() => {
    formModal = false;
    if (message != null) {
      let mountPoint: any = document.getElementById("toast");

      const app = mount(Toast, { target: mountPoint, props: { message } });
    }
    return unsubscribe;
  });
</script>

<Table shadow hoverable={true}>
  <TableHead class="bg-custom-brown text-white overflow-x-auto">
    <TableHeadCell>ID</TableHeadCell>
    <TableHeadCell>Description</TableHeadCell>
    <TableHeadCell>Location</TableHeadCell>
    <TableHeadCell>Number of parking spots</TableHeadCell>
    <TableHeadCell>Actions</TableHeadCell>
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
              >
                View {cell}
              </a></TableBodyCell
            >
          {/if}
        {/each}
        <TableBodyCell tdClass="gap-2">
          <form method="post" action="?/doAction">
            <Button
              on:click={() => {
                formModal = true;
                itemToEdit = row;
              }}
              name="edit"
              pill
              color="alternative"
            >
              Edit
            </Button>
            <input type="hidden" name="ps_id" value={row.ps_id} />
            <Button
              type="submit"
              formaction="?/delete"
              name="delete"
              pill
              color="red"
            >
              Delete
            </Button>
          </form>
        </TableBodyCell>
      </TableBodyRow>
    {/each}
  </TableBody>
</Table>

<Modal bind:open={formModal} size="xs" autoclose={false}>
  <form class="flex flex-col space-y-6" method="post" action="?/doAction">
    <input type="hidden" name="ps_id" value={itemToEdit.ps_id} />
    <h3 class="mb-4 text-xl font-medium text-gray-900 dark:text-white">
      Edit : {itemToEdit.ps_id}
    </h3>
    <Label class="space-y-2">
      <span>Description</span>
      <Input
        type="text"
        name="ps_description"
        value={itemToEdit.ps_description}
        required
      />
    </Label>
    <Label class="space-y-2">
      <span>Number of parking spots available</span>
      <Input
        type="number"
        name="ps_number"
        value={itemToEdit.ps_max_parking_spots}
        required
      />
    </Label>
    <div class="flex flex-col-2 justify-center gap-4">
      <Button type="submit" pill color="green">Save</Button>
      <Button pill color="alternative" on:click={() => (formModal = false)}>
        Cancel
      </Button>
    </div>
  </form>
</Modal>

<div id="toast"></div>
