<script lang="ts">
  import { signOut } from "@auth/sveltekit/client"
  import { page } from '$app/stores';  
 
  var baseUrl = $page.url.origin;
</script>


<h1>This is the SignOut page</h1>

<button on:click={() => signOut({callbackUrl :  baseUrl})}>
  Sign Out
</button>