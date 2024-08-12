import * as db from "$lib/Utils";
import { json } from "@sveltejs/kit";

export async function POST({ request }) {
  const { cm_id } = await request.json();
  let cam = await db.getPolygon(cm_id);
  console.log(cam);
  return json({ cam }, { status: 201 });
}
