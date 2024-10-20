<script lang="ts">
  import { Toast, type ColorVariant } from "flowbite-svelte";
  import { CheckCircleSolid } from "flowbite-svelte-icons";
  import { onMount, unmount } from "svelte";
  import { slide } from "svelte/transition";
  let { message = "" } = $props();
  let longMessage = "Operation Status:" + message;

  let toastStatus = $state(false);
  let counter = 0;
  const colorComp = $derived(message == "OK" ? "green" : "red");

  function trigger() {
    counter = 3;
    toastStatus = true;
    timeout();
  }
  function timeout() {
    if (--counter > 0) return setTimeout(timeout, 1000);
    toastStatus = false;
  }

  onMount(() => {
    trigger();
  });
</script>

<Toast
  transition={slide}
  bind:toastStatus
  position="top-right"
  color={colorComp}
>
  <CheckCircleSolid slot="icon" class="w-5 h-5" />
  {longMessage}
</Toast>
