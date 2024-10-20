<script lang="ts">
  // import Chart from "../../lib/components/Chart.svelte";
  import { writable } from "svelte/store";
  import type { PageData } from "./$types";
  import { onMount } from "svelte";
  import Spinner from "$lib/components/Spinner.svelte";
  import { Chart, Card } from "flowbite-svelte";
  import { FlagOutline, UsersGroupOutline } from "flowbite-svelte-icons";
  const chartOptions: any = writable({
    colors: ["#1A56DB"],
    series: [
      {
        name: "Traffic Violations",
        color: "#1A56DB",
        data: [],
      },
    ],
    chart: {
      type: "bar",
      height: "320px",
      fontFamily: "Inter, sans-serif",
      toolbar: {
        show: false,
      },
    },
    noData: {
      text: "Loading...",
    },
    plotOptions: {
      bar: {
        horizontal: false,
        columnWidth: "70%",
        borderRadiusApplication: "end",
        borderRadius: 8,
      },
    },
    tooltip: {
      shared: true,
      intersect: false,
      style: {
        fontFamily: "Inter, sans-serif",
      },
    },
    states: {
      hover: {
        filter: {
          type: "darken",
          value: 1,
        },
      },
    },
    stroke: {
      show: true,
      width: 0,
      colors: ["transparent"],
    },
    grid: {
      show: false,
      strokeDashArray: 4,
      padding: {
        left: 2,
        right: 2,
        top: -14,
      },
    },
    dataLabels: {
      enabled: false,
    },
    legend: {
      show: false,
    },
    xaxis: {
      floating: false,
      labels: {
        show: true,
        style: {
          fontFamily: "Inter, sans-serif",
          cssClass: "text-xs font-normal fill-gray-500 dark:fill-gray-400",
        },
      },
      axisBorder: {
        show: false,
      },
      axisTicks: {
        show: false,
      },
    },
    yaxis: {
      show: false,
    },
    fill: {
      opacity: 1,
    },
  });
  const chartOptions1: any = writable({
    colors: ["#1A56DB"],
    series: [
      {
        name: "Traffic Violations",
        color: "#1A56DB",
        data: [],
      },
    ],
    chart: {
      type: "bar",
      height: "320px",
      fontFamily: "Inter, sans-serif",
      toolbar: {
        show: false,
      },
    },
    noData: {
      text: "Loading...",
    },
    plotOptions: {
      bar: {
        horizontal: false,
        columnWidth: "70%",
        borderRadiusApplication: "end",
        borderRadius: 8,
      },
    },
    tooltip: {
      shared: true,
      intersect: false,
      style: {
        fontFamily: "Inter, sans-serif",
      },
    },
    states: {
      hover: {
        filter: {
          type: "darken",
          value: 1,
        },
      },
    },
    stroke: {
      show: true,
      width: 0,
      colors: ["transparent"],
    },
    grid: {
      show: false,
      strokeDashArray: 4,
      padding: {
        left: 2,
        right: 2,
        top: -14,
      },
    },
    dataLabels: {
      enabled: false,
    },
    legend: {
      show: false,
    },
    xaxis: {
      floating: false,
      labels: {
        show: true,
        style: {
          fontFamily: "Inter, sans-serif",
          cssClass: "text-xs font-normal fill-gray-500 dark:fill-gray-400",
        },
      },
      axisBorder: {
        show: false,
      },
      axisTicks: {
        show: false,
      },
    },
    yaxis: {
      show: false,
    },
    fill: {
      opacity: 1,
    },
  });
  export let data: PageData;
  let totalTrafficViolations: number = 0;
  let totalTrafficViolations3: number = 0;
  onMount(() => {
    let dataJson: {
      TrafficViolationStats: any;
      TrafficViolationStats1: any;
      TrafficViolationStats2: any;
      TrafficViolationStats3: any;
    } = JSON.parse(data.stats);
    let dataParking: any = [];
    dataJson.TrafficViolationStats.forEach((element: any[]) => {
      dataParking.push({ x: element[0], y: element[1] });
      totalTrafficViolations = totalTrafficViolations + element[1];
    });
    chartOptions.update((opts: { series: { data: any }[] }) => {
      opts.series[0].data = dataParking;
      return opts;
    });

    dataParking = [];
    dataJson.TrafficViolationStats3.forEach((element: any[]) => {
      dataParking.push({ x: element[0], y: element[1] });
      totalTrafficViolations3 = totalTrafficViolations3 + element[1];
    });
    chartOptions1.update((opts: { series: { data: any }[] }) => {
      opts.series[0].data = dataParking;
      return opts;
    });
    return chartOptions;
  });
</script>

<title>Statistics</title>
<header>
  <h1>Statistics</h1>
</header>
<!--
{#if $infractionsStore !== null}
  <Chart {infractionsStore} />
{:else}
  <Spinner />
{/if}
-->
{#if $chartOptions !== null}
  <div class="flex flex-wrap justify-between gap-3 pb-4 mb-4">
    <Card>
      <div
        class="flex justify-between pb-4 mb-4 border-b border-gray-200 dark:border-gray-700"
      >
        <div class="flex items-center">
          <div
            class="w-12 h-12 rounded-lg bg-gray-100 dark:bg-gray-700 flex items-center justify-center me-3"
          >
            <FlagOutline class="w-6 h-6 text-gray-500 dark:text-gray-400" />
          </div>
          <div>
            <h5
              class="leading-none text-2xl font-bold text-gray-900 dark:text-white pb-1"
            >
              Total : {totalTrafficViolations}
            </h5>
            <p class="text-sm font-normal text-gray-500 dark:text-gray-400">
              Traffic Violations per Zone
            </p>
          </div>
        </div>
      </div>

      <Chart id="test1" options={$chartOptions} />
    </Card>
    {#each Array(10) as _, index (index)}
      <Card>
        <div
          class="flex justify-between pb-4 mb-4 border-b border-gray-200 dark:border-gray-700"
        >
          <div class="flex items-center">
            <div
              class="w-12 h-12 rounded-lg bg-gray-100 dark:bg-gray-700 flex items-center justify-center me-3"
            >
              <FlagOutline class="w-6 h-6 text-gray-500 dark:text-gray-400" />
            </div>
            <div>
              <h5
                class="leading-none text-2xl font-bold text-gray-900 dark:text-white pb-1"
              >
                Total : {totalTrafficViolations3}
              </h5>
              <p class="text-sm font-normal text-gray-500 dark:text-gray-400">
                Traffic Violations over a period of time
              </p>
            </div>
          </div>
        </div>

        <Chart id="test" options={$chartOptions1} />
      </Card>
    {/each}
  </div>
{:else}
  <Spinner />
{/if}
