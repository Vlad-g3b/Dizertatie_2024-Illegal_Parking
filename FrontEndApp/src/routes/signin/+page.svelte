<script lang="ts">
  import { signIn, signOut } from "@auth/sveltekit/client"
  import {page} from "$app/stores"
  import { goto } from "$app/navigation";
  async function handleClick(){
    try {
      await signIn("github");
      goto("/authenticated/dashboard")
    } catch(error){
      console.error('Error signing out:', error);
    }
  }
</script>
<title> HomePage </title>
<nav>
<h1> Smart on StreetParking </h1>

<div class="actions">
  {#if $page.data.session == null}
  <div class="wrapper-form">
    <button on:click={() => signIn( "github",{callbackUrl: $page.url.origin + "/admin/dashboard"})}>Sign In with GitHub</button>
  </div>
  {:else}
  Wellcome {$page.data.session.user?.name}
 <button on:click={() => goto("/signout")}>
    Sign Out
  </button>
  {/if}
</div>
</nav>