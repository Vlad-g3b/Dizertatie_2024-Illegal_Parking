<script lang="ts">
  import { Bar } from "svelte-chartjs";
  import { data } from "./data.js";
  import { onMount } from "svelte";
  var mydata = "None";
  import {
    Chart,
    Title,
    Tooltip,
    Legend,
    BarElement,
    CategoryScale,
    LinearScale,
  } from "chart.js";
  Chart.register(
    Title,
    Tooltip,
    Legend,
    BarElement,
    CategoryScale,
    LinearScale
  );
  export let infractionsStore: any;
  let tf_list: any;

  const unsubscribe = infractionsStore.subscribe((data: any) => {
    tf_list = data;
  });

  console.log(data);
  function getRandomRGBA() {
    var r = Math.floor(Math.random() * 256); // Random value between 0 and 255 for red
    var g = Math.floor(Math.random() * 256); // Random value between 0 and 255 for green
    var b = Math.floor(Math.random() * 256); // Random value between 0 and 255 for blue
    var a = 0.5; // Random value between 0 and 1 for alpha (opacity)

    return "rgba(" + r + "," + g + "," + b + "," + a + ")";
  }
  onMount(() => {
    console.log("liost", tf_list);
    var mydata = JSON.parse(tf_list).TrafficViolationStats;
    var labels: any[] = [];
    var values: any[] = [];
    var backgroundColor: string[] = [];
    mydata.forEach((element: any[]) => {
      console.log(element);
      labels.push(element[0]);
      values.push(element[1]);
      var randomColor = getRandomRGBA();
      backgroundColor.push(randomColor);
    });

    data.labels = labels;
    data.datasets[0].data = values;
    data.datasets[0].backgroundColor = backgroundColor;

    console.log(data);
    return unsubscribe;
  });
</script>

<Bar {data} options={{ responsive: true }} />
