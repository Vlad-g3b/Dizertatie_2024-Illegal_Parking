<script lang="ts">
  import { onMount } from "svelte";
  import L from "leaflet";
  import "leaflet/dist/leaflet.css";
  import "leaflet.heat";
  import "leaflet.heat?client"; //
  import { toast } from "@zerodevx/svelte-toast";
  import * as turf from "@turf/turf";
  import type { HeatLayer, LatLngBoundsExpression, Layer, Map } from "leaflet";

  export let latitude: number;
  export let longitude: number;
  export let infractionsStore: any;
  let list: any;
  let map: L.Map;
  let Leaflet;
  let heatLayer: typeof HeatLayer;
  let randomPointInPoly = function (polygon: {
    getBounds: () => any;
    toGeoJSON: () => any;
  }) {
    var bounds = polygon.getBounds();
    var x_min = bounds.getEast();
    var x_max = bounds.getWest();
    var y_min = bounds.getSouth();
    var y_max = bounds.getNorth();

    var lat = y_min + Math.random() * (y_max - y_min);
    var lng = x_min + Math.random() * (x_max - x_min);
    var point = turf.point([lng, lat]);
    var poly = polygon.toGeoJSON();
    var inside = turf.inside(point, poly);
    if (inside) {
      return point;
    } else {
      return randomPointInPoly(polygon);
    }
  };

  function addFakePoints(heatL: never[][], poll: any) {
    for (let index = 0; index < 20; index++) {
      var point = randomPointInPoly(poll);
      let coordinates = point.geometry.coordinates.reverse();
      let newArray: any = [];
      newArray = newArray.concat(coordinates, 0.2);
      heatL.push(newArray);
    }
    return heatL;
  }

  function createFakeLines(La: typeof L) {
    let heatL: never[][] = [];
    var latlngs: LatLngBoundsExpression = [
      [38.24342665110504, 21.732123117195943],
      [38.24397197980599, 21.732811804564857],
      [38.24401323644827, 21.732748603592494],
      [38.243467725225884, 21.732076950954465],
      [38.24342665110504, 21.732123117195943],
    ];
    La.polygon(latlngs, { color: "red" }).addTo(map);
    latlngs = [
      [38.246676750616274, 21.736152262797702],
      [38.24661018382857, 21.736259134505573],
      [38.247165869926, 21.737010921691972],
      [38.24726716641305, 21.736889309058878],
      [38.246676750616274, 21.736152262797702],
    ];
    let poll = L.polygon(latlngs, { color: "green" }).addTo(map);
    heatL = addFakePoints(heatL, poll);

    latlngs = [
      [38.24539178223797, 21.734483343711513],
      [38.2453102994774, 21.734591605801274],
      [38.245707084233544, 21.735101339807244],
      [38.24576022488465, 21.734984055876662],
      [38.24539178223797, 21.734483343711513],
    ];
    poll = L.polygon(latlngs, { color: "blue" }).addTo(map);
    heatL = addFakePoints(heatL, poll);
    latlngs = [
      [38.24478951618356, 21.733693932631247],
      [38.2446761479004, 21.733833771163855],
      [38.24523590207996, 21.734510409224875],
      [38.24534926949015, 21.734415679896337],
      [38.24478951618356, 21.733693932631247],
    ];
    poll = L.polygon(latlngs, { color: "yellow" }).addTo(map);
    heatL = addFakePoints(heatL, poll);
    latlngs = [
      [38.245313842193454, 21.73308946929674],
      [38.245207560199766, 21.73325637335179],
      [38.24574959674297, 21.733919478651586],
      [38.245855877944145, 21.733793172880194],
      [38.245313842193454, 21.73308946929674],
    ];
    poll = L.polygon(latlngs, { color: "black" }).addTo(map);
    heatL = addFakePoints(heatL, poll);
    return heatL;
  }
  infractionsStore.subscribe((infractions: any) => {
    // Clear existing markers
    list = infractions;
    let infractionsJSon = JSON.parse(infractions);
    infractionsJSon.TrafficViolationList.forEach(
      (infraction: { location: Array<number>; id: any }) => {
        toast.push(`<div>Detected ${infraction.id} </div>`, {
          theme: {
            "--toastColor": "mintcream",
            "--toastBackground": "rgba(72,187,120,0.9)",
            "--toastBarBackground": "#2F855A",
          },
        });
      }
    );
  });
  onMount(async () => {
    if (typeof window !== "undefined") {
      import("leaflet").then(async (L) => {
        map = L.map("map").setView([latitude, longitude], 16);
        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
          attribution: "&copy; OpenStreetMap contributors",
        }).addTo(map);
        var myList = JSON.parse(list).TrafficViolationList;
        let heatL = createFakeLines(L);
        myList.forEach((element: any) => {
          let newArray: any = [];
          newArray = newArray.concat(element.location, 0.2);
          heatL.push(newArray);
          let markcoord = element.location;
          let content = `<div>ID:${element.id} Description:${element.description}</div>
                        <form  method="post" action="?/resolveTf">
                        <input type="hidden" name="id" value=${element.id} />
                        <input type='submit' value="Mark as resolved!"/>
                        </from>`;
          let marker = L.marker([markcoord[0], markcoord[1]])
            .addTo(map)
            .bindPopup(content);
          // marker.infractionId = element.id;
        });
        L.heatLayer(heatL, { radius: 20 }).addTo(map);
        const unsubscribe = infractionsStore.subscribe((infractions: any) => {
          // Clear existing markers
          let infractionsJSon = JSON.parse(infractions);
          console.log(infractionsJSon);
          infractionsJSon.TrafficViolationList.forEach(
            (infraction: {
              description: any;
              location: Array<never>;
              id: any;
            }) => {
              let arr: any = [
                infraction.location[0],
                infraction.location[1],
                0.2,
              ];
              heatL.push(arr);
              let marker = L.marker([
                infraction.location[0],
                infraction.location[1],
              ])
                .addTo(map)
                .bindPopup(
                  `<div>ID:${infraction.id} Description:${infraction.description}</div>
                  <form  method="post" action="?/resolveTf">
                  <input type="hidden" name="id" value=${infraction.id} />
                  <input type='submit' value="Mark as resolved!"/>
                  </from>`
                );

              // Store infraction ID in marker for identification
              //  marker.infractionId = infraction.id;
            }
          );
        });
        return unsubscribe;
      });
    }
  });
</script>

<div id="map"></div>

<style>
  #map {
    height: 100%;
  }
</style>
