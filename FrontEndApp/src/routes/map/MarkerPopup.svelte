<script lang="ts">
  import { Button } from "flowbite-svelte";
  export let infraction: any;
  console.log(infraction);
</script>

<div class="text-wrap flex flex-col">
  <p class="">
    ID:{infraction.id} Description: {infraction.description}
  </p>
  <form
    class="flex justify-center items-center"
    method="post"
    action="?/resolveTf"
  >
    <input type="hidden" name="id" value="${infraction.id}" />
    <Button class="" pill type="submit">Mark as resolved!</Button>
  </form>
</div>
