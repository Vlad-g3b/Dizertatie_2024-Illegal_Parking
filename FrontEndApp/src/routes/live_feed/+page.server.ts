import * as db from "$lib/Utils";
import { error } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({}) => {
  const polygon = await db.getAllPolygons();
  return { polygon };
};
export const actions = {
  savePolygon: async ({ request, locals }) => {
    const formData = await request.formData();
    const session = await locals.auth();
    let id: number | undefined;
    let formId = formData.get("id");
    if (formId != null) {
      id = Number.parseInt(formId.toString());
    }
    const polygon: string | undefined = formData.get("polygon")?.toString();
    const ps_id: string | undefined = formData.get("ps_id")?.toString();
    if (typeof id === "undefined") {
      return error(400, {
        message: "Something went wrong...",
      });
    }
    db.insertOrUpdatePolygon(id, ps_id, polygon, session?.user?.name);
  },
};
