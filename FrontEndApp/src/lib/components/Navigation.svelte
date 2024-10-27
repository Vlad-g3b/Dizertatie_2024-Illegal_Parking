<script lang="ts">
  import "../../routes/styles.css";
  import { page } from "$app/stores";
  import { signIn, signOut } from "@auth/sveltekit/client";
  import {
    Sidebar,
    SidebarGroup,
    SidebarItem,
    SidebarWrapper,
    Avatar,
    Button,
  } from "flowbite-svelte";
  import {
    ChartPieSolid,
    GlobeOutline,
    VideoCameraOutline,
    ExclamationCircleSolid,
    MapPinAltOutline,
    ScaleBalancedOutline,
  } from "flowbite-svelte-icons";
  let adminPath = $page.data.session?.user == null ? "user/" : "admin/";
  let homePage = $page.data.session?.user == null ? "/" : "/admin/dashboard";
  $: activeUrl = $page.url.pathname;
  let divClass =
    "overflow-y-auto py-4 px-3 bg-custom-brown size-full dark:bg-gray-800";
  let activeClass =
    "flex items-center p-2 text-base font-normal text-primary-900 bg-primary-200 rounded-lg hover:bg-primary-100";
  let nonActiveClass =
    "flex items-center p-2 text-base font-normal text-white rounded-lg hover:text-custom-brown hover:bg-cutom-brown-light";
</script>

<Sidebar {activeUrl} {activeClass} {nonActiveClass}>
  <SidebarWrapper {divClass}>
    <SidebarGroup>
      {#if $page.data.session != null}
        <div class="flex items-center space-x-4 rtl:space-x-reverse">
          <Avatar src={$page.data.session.user?.image} rounded />
          <div class="space-y-1 font-medium text-white">
            <div class="text-md font-bold">{$page.data.session.user?.name}</div>
            <div class="text-sm">Welcome!</div>
          </div>
          <div class="space-y-1">
            <Button on:click={() => signOut({ callbackUrl: $page.url.origin })}>
              Sign Out
            </Button>
          </div>
        </div>
      {:else}
        <div class="lex items-center space-x-4 rtl:space-x-reverse">
          <Button on:click={() => signIn("github")}>Sign In</Button>
        </div>
      {/if}
      <SidebarItem label="Dashboard" href={homePage}>
        <svelte:fragment slot="icon">
          <ChartPieSolid class="w-6 h-6" />
        </svelte:fragment>
      </SidebarItem>
      <SidebarItem label="Live Map" href="/map">
        <svelte:fragment slot="icon">
          <GlobeOutline class="w-6 h-6" />
        </svelte:fragment>
      </SidebarItem>
      <SidebarItem label="Live Feed" href="/live_feed">
        <svelte:fragment slot="icon">
          <VideoCameraOutline class="w-6 h-6" />
        </svelte:fragment>
      </SidebarItem>
      {#if $page.data.session?.user != null}
        <SidebarItem label="Traffic Violations" href="/{adminPath}tf_list">
          <svelte:fragment slot="icon">
            <ExclamationCircleSolid class="w-6 h-6" />
          </svelte:fragment>
        </SidebarItem>
      {/if}
      <SidebarItem label="Parking Sites" href="/{adminPath}ps_list">
        <svelte:fragment slot="icon">
          <MapPinAltOutline class="w-6 h-6" />
        </svelte:fragment>
      </SidebarItem>
      <SidebarItem label="Statistics" href="/statistics">
        <svelte:fragment slot="icon">
          <ScaleBalancedOutline class="w-6 h-6" />
        </svelte:fragment>
      </SidebarItem>
    </SidebarGroup>
  </SidebarWrapper>
</Sidebar>
