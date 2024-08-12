<script lang="ts">
  import { onMount } from "svelte";
  import { Button } from "flowbite-svelte";
  export let tf_store: any;
  let tf_list: any;

  const unsubscribe = tf_store.subscribe((data: any) => {
    tf_list = data;
  });

  onMount(() => {
    return unsubscribe;
  });
</script>

<form method="POST">
  <table>
    <thead>
      <tr>
        <th>ID</th>
        <th>Description</th>
        <th>Location</th>
        <th>Recorded Date</th>
        <th>Resolved Date</th>
        <th>Resolved By</th>
        <th>Status</th>
      </tr>
    </thead>
    <tbody>
      {#each tf_list.TrafficViolationList as tf}
        <tr>
          <td>{tf.id}</td>
          <td>{tf.description}</td>
          <td>
            <a href="https://www.google.com/maps/place/{tf.location}"> View </a>
          </td>
          <td>{tf.date_ins}</td>
          <td>{tf.date_res}</td>
          <td>{tf.username}</td>
          <td>
            <form method="post" action="?/resolveTf">
              {#if tf.resolved == 0}
                <input type="hidden" name="id" value={tf.id} />
                <Button pill type="submit">Resolve...</Button>
                <!-- <button on:click={() => doPost(tf)}> Resolve... </button> -->
              {:else}
                Resolved
              {/if}
            </form>
          </td>
        </tr>
      {/each}
    </tbody>
  </table>
</form>

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
