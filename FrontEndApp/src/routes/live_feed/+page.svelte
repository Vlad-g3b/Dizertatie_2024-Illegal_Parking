<script lang="ts">
  import { Video, Button } from "flowbite-svelte";
  import { onMount } from "svelte";
  import { Card } from "flowbite-svelte";
  import type { PageData } from "./$types";
  export let data: PageData;
  let video_sources = [
    {
      src: "/assets/video1.mp4",
      id: "video1.mp4",
      cm_id: 1,
      ps_id: "ParkingSite_1707850206",
    },
    {
      src: "/assets/video2.mp4",
      id: "video2.mp4",
      cm_id: 3,
      ps_id: "ParkingSite_1707851774",
    },
    {
      src: "/assets/video2.mp4",
      id: "video4.mp4",
      cm_id: 4,
      ps_id: "ParkingSite_1707851774",
    },
    {
      src: "/assets/video2.mp4",
      id: "video5.mp4",
      cm_id: 5,
      ps_id: "ParkingSite_1707851774",
    },
    {
      src: "/assets/video2.mp4",
      id: "video5.mp4",
      cm_id: 5,
      ps_id: "ParkingSite_1707851774",
    },

    {
      src: "/assets/video2.mp4",
      id: "video5.mp4",
      cm_id: 5,
      ps_id: "ParkingSite_1707851774",
    },
    {
      src: "/assets/video2.mp4",
      id: "video5.mp4",
      cm_id: 5,
      ps_id: "ParkingSite_1707851774",
    },
    {
      src: "/assets/video2.mp4",
      id: "video5.mp4",
      cm_id: 5,
      ps_id: "ParkingSite_1707851774",
    },
  ];

  let showPopup = false;
  let screenshotSrc = "";
  let canvas: HTMLCanvasElement;
  let ctx: any;
  let isDrawing = false;
  let image: any = null;
  let startPoint = { x: 0, y: 0 };
  let lines: any = []; // Array to store line points
  let lastPoint: any = null;
  let isShapeClosed = false;
  let strokeColor = "#F6F6F3"; // Default stroke color
  let strokeWidth = 4; // Default stroke width
  let videoID: any;
  let apiList: any;
  async function getPolygon(cm_id: any) {
    const response = await fetch("/admin/api/get_polygon", {
      method: "POST",
      body: JSON.stringify({ cm_id: cm_id }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    return response.json();
  }
  async function takeScreenshot(videoId: string, cm_id: any) {
    lines = [];
    lastPoint = null;
    isShapeClosed = false;
    videoID = videoId;
    let response = await getPolygon(cm_id);
    console.log(response);
    startPoint = { x: 0, y: 0 };
    const videoElement = <HTMLVideoElement>document.getElementById(videoId);
    const canvas = document.createElement("canvas");
    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;
    let lineList = JSON.parse(response.cam.cm_polygon);
    console.log(lineList);
    apiList = lineList;
    const context = <CanvasRenderingContext2D>canvas.getContext("2d");
    context.strokeStyle = strokeColor; // Use current stroke color
    context.lineWidth = strokeWidth; // Use current stroke width
    context?.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
    screenshotSrc = canvas.toDataURL("image/png");
    showPopup = true;
    image.src = screenshotSrc;
  }

  function closePopup() {
    showPopup = false;
    screenshotSrc = "";
  }

  function getMousePosition(event: any) {
    const rect = canvas.getBoundingClientRect();
    return {
      x: event.clientX - rect.left,
      y: event.clientY - rect.top,
    };
  }

  function saveScreenshot() {
    //  const link = document.createElement("a");
    //  link.href = screenshotSrc;
    //  link.download = "screenshot.png";
    //  link.click();
    if (!isShapeClosed) {
      closeShape();
    }
    const polygonInput = <HTMLInputElement>(
      document.querySelector("input[name='polygon']")
    );
    let outputList: Array<Array<Number>> = [];
    if (polygonInput) {
      lines.forEach(
        (line: { start: { x: any; y: any }; end: { x: any; y: any } }) => {
          console.log(line.start, line.end);
          outputList.push([Math.round(line.start.x), Math.round(line.start.y)]);
        }
      );
      console.log(JSON.stringify(outputList));
      polygonInput.value = JSON.stringify(outputList);
    }
    const id = <HTMLInputElement>document.querySelector("input[name='id']");
    const psId = <HTMLInputElement>(
      document.querySelector("input[name='ps_id']")
    );
    for (let vid of video_sources) {
      if (vid.id == videoID) {
        id.value = vid.cm_id.toString();
        psId.value = vid.ps_id;
      }
    }
    //closePopup();
  }
  function clearCanvas() {
    if (ctx) {
      ctx.drawImage(image, 0, 0, canvas.width, canvas.height);
      lines = [];
      lastPoint = null;
      isShapeClosed = false;
      startPoint = { x: 0, y: 0 };
    }
  }
  function startDrawing(event: any) {
    if (!showPopup) return;
    isDrawing = true;
    // Use lastPoint as startPoint if available, else use current mouse position
    startPoint = lastPoint || getMousePosition(event);
    ctx.strokeStyle = strokeColor; // Use current stroke color
    ctx.lineWidth = strokeWidth; // Use current stroke width
  }

  function drawLine(event: any) {
    if (!isDrawing) return;
    const { x, y } = getMousePosition(event);

    // Clear the canvas and redraw the image and lines
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(image, 0, 0, canvas.width, canvas.height);

    // Redraw existing lines
    lines.forEach(
      (line: { start: { x: any; y: any }; end: { x: any; y: any } }) => {
        ctx.beginPath();
        ctx.moveTo(line.start.x, line.start.y);
        ctx.lineTo(line.end.x, line.end.y);
        ctx.stroke();
        ctx.closePath();
      }
    );

    // Draw the current line
    ctx.beginPath();

    ctx.moveTo(startPoint.x, startPoint.y);
    ctx.lineTo(x, y);
    ctx.stroke();
    ctx.closePath();
  }

  function stopDrawing(event: any) {
    if (!isDrawing) return;
    isDrawing = false;
    const endPoint = getMousePosition(event);

    // Store the line
    lines.push({ start: startPoint, end: endPoint });
    console.log(lines);
    // Update lastPoint to the end of the current line
    lastPoint = endPoint;

    // Draw the final line
    ctx.beginPath();
    ctx.moveTo(startPoint.x, startPoint.y);
    ctx.lineTo(endPoint.x, endPoint.y);
    ctx.stroke();
    ctx.closePath();
  }

  function closeShape() {
    if (lines.length > 1) {
      const firstPoint = lines[0].start;
      const lastPointL = lines[lines.length - 1].end;

      // Draw the closing line
      ctx.beginPath();
      ctx.moveTo(lastPointL.x, lastPointL.y);
      ctx.lineTo(firstPoint.x, firstPoint.y);
      ctx.stroke();
      ctx.closePath();

      // Add the closing line to the lines array
      lines.push({ start: lastPointL, end: firstPoint });

      // Reset lastPoint
      lastPoint = null;
      isShapeClosed = true;
    }
  }

  // Handle Ctrl + Click to close the shape
  function handleMouseDown(event: { ctrlKey: any }) {
    if (event.ctrlKey) {
      closeShape();
    } else {
      startDrawing(event);
    }
  }

  onMount(() => {
    image = new Image();
    console.log("call onMount before img load...");
    image.onload = () => {
      // Once the image is loaded, draw it on the canvas
      if (canvas) {
        ctx = canvas.getContext("2d");
        canvas.width = image.width;
        canvas.height = image.height;
        let lineList = apiList;
        ctx.strokeStyle = strokeColor; // Use current stroke color
        ctx.lineWidth = strokeWidth;
        ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas
        ctx.drawImage(image, 0, 0, canvas.width, canvas.height);
        for (let i = 0; i < lineList.length; i++) {
          const start = lineList[i];
          const end = lineList[(i + 1) % lineList.length]; // Loop back to the start to close the shape

          ctx.beginPath();
          ctx.moveTo(start[0], start[1]);
          ctx.lineTo(end[0], end[1]);
          ctx.stroke();
          ctx.closePath();

          // Store the line in the `lines` array
        }
        console.log("call onMount...");
      }
    };
  });
</script>

<div class="flex justify-center items-center">
  <div class="grid grid-cols-4 gap-4 items-center">
    {#each video_sources as video}
      <Card class="flex flex-col gap-2 items-center">
        <div class="">
          <Video
            id={video.id}
            src={video.src}
            muted
            controls
            trackSrc={video.id}
          />
        </div>
        <p class="mb-3">Description: add something later...</p>
        <div>
          <Button pill on:click={() => takeScreenshot(video.id, video.cm_id)}>
            Modify Limits
          </Button>
        </div>
      </Card>
    {/each}
  </div>
</div>
{#if showPopup}
  <div class="popup grid grid-flow-row gap-4 auto-rows-max">
    <!-- svelte-ignore a11y-mouse-events-have-key-events -->
    <div>
      <canvas
        bind:this={canvas}
        on:mousedown={handleMouseDown}
        on:mousemove={drawLine}
        on:mouseup={stopDrawing}
        on:mouseout={stopDrawing}
      >
      </canvas>
    </div>

    <div
      class="flex grid grid-flow-col auto-cols-max gap-4 justify-center item-center"
    >
      <Button on:click={closePopup}>Cancel</Button>
      <Button on:click={clearCanvas}>Clear</Button>
      <form method="post" action="?/savePolygon">
        <input type="hidden" name="id" />
        <input type="hidden" name="ps_id" />
        <input type="hidden" name="polygon" />
        <Button type="submit" name="cam1" on:click={saveScreenshot}>
          Save
        </Button>
      </form>
    </div>
  </div>
{/if}

<style>
  .popup {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    padding: 20px;
    background-color: white;
    border: 1px solid black;
    z-index: 1000;
  }
</style>
