<script lang="ts">
  import {
    Avatar,
    Button,
    Card,
    Listgroup,
    ListgroupItem,
    type ListGroupItemType,
  } from "flowbite-svelte";
  import type { PageData } from "./$types";
  export let data: PageData;
  interface listItemNews extends ListGroupItemType {
    id: any;
    description: any;
    date_ins: any;
    location: any;
  }
  let listNews: listItemNews[] = data.latestNews;
  let listUser: any = data.users;
</script>

<title> HomePage ADMIN</title>
<nav>
  <h1>Dashboard</h1>
</nav>
<div class="flex justify-center items-center">
  <div class="grid grid-cols-3 gap-4 items-top">
    <Card padding="xl">
      <div class="flex justify-between items-center mb-4">
        <h5
          class="text-xl font-bold leading-none text-gray-900 dark:text-white"
        >
          Latest Notifications
        </h5>
        <a
          href="/admin/tf_list"
          class="text-sm font-medium text-primary-600 hover:underline dark:text-primary-500"
        >
          View all
        </a>
      </div>
      <Listgroup class="border-0 dark:!bg-transparent ">
        {#each listNews as item}
          <ListgroupItem class="px-0">
            <div class="flex items-center space-x-4 rtl:space-x-reverse">
              <div class="flex-1 min-w-0">
                <p
                  class="text-sm font-medium text-gray-900 truncate dark:text-white"
                >
                  {item.id}
                </p>
                <p class="text-sm text-gray-500 truncate dark:text-gray-400">
                  {item.description}
                </p>
              </div>
              <div
                class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white"
              >
                <a
                  href={`/map?lat=${item.location[0]}&lng=${item.location[1]}`}
                >
                  View
                </a>
              </div>
            </div>
          </ListgroupItem>
        {/each}
      </Listgroup>
    </Card>

    <Card padding="xl" class="h-16 md:h-27 lg:h-64">
      <div class="flex justify-between items-center mb-4">
        <h5
          class="text-xl font-bold leading-none text-gray-900 dark:text-white"
        >
          Active Users
        </h5>
      </div>
      <Listgroup
        class="border-0 dark:!bg-transparent overflow-auto overflow-hidden hover:overflow-y-scroll"
      >
        {#each listUser as user}
          <ListgroupItem class="px-0">
            <div class="flex items-center space-x-4 rtl:space-x-reverse">
              <Avatar
                src={user.usr_profile_pic}
                alt="profile picc"
                class="flex-shrink-0"
              />
              <div class="flex-1 min-w-0">
                <p
                  class="text-sm font-medium text-gray-900 truncate dark:text-white"
                >
                  {user.usr_name}
                </p>
                <p class="text-sm text-gray-500 truncate dark:text-gray-400">
                  {user.usr_email}
                </p>
              </div>
              <div
                class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white"
              ></div>
            </div>
          </ListgroupItem>
        {/each}
      </Listgroup>
    </Card>
    <Card padding="xl">
      <div class="flex justify-between items-center mb-4">
        <h5
          class="text-xl font-bold leading-none text-gray-900 dark:text-white"
        >
          Actions
        </h5>
      </div>
      <div
        class="grid grid-rows-4 grid-flow-col gap-4 border-0 dark:!bg-transparent"
      >
        <Button color="blue">View Logs</Button>
        <Button color="green">Add Notes</Button>
        <Button color="red">Delete Notes</Button>
        <Button color="blue">View Logs</Button>
        <Button color="blue">View Logs</Button>
        <Button color="blue">View Logs</Button>
        <Button color="blue">View Logs</Button>
        <Button color="blue">View Logs</Button>
      </div>
    </Card>
    <div class="col-span-3 size-full w-full">
      <Card padding="xl" class="w-full size-full max-w-full">
        <div class="flex justify-between items-center mb-4 ">
          <h5
            class="text-xl font-bold leading-none text-gray-900 dark:text-white"
          >
            Actions
          </h5>
        </div>
        <div
          class="grid grid-rows-4 grid-flow-col gap-4 border-0 dark:!bg-transparent"
        >
          <Button color="blue">View Logs</Button>
          <Button color="green">Add Notes</Button>
          <Button color="red">Delete Notes</Button>
          <Button color="blue">View Logs</Button>
          <Button color="blue">View Logs</Button>
          <Button color="blue">View Logs</Button>
          <Button color="blue">View Logs</Button>
          <Button color="blue">View Logs</Button>
        </div>
      </Card>
    </div>
  </div>
</div>
