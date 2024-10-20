import * as db from "$lib/Utils";
import { error } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";
let message: any = "";
export const load: PageServerLoad = async ({}) => {
  const parkingSites = await db.getAllTParkingSites();
  console.log("from loadPage");
  return { parkingSites };
};
export const actions = {
  doAction: async ({ request }) => {
    const formData = await request.formData();
    const ps_id: string | undefined = formData.get("ps_id")?.toString();
    message = "OK";
    const ps_description: string | undefined = formData
      .get("ps_description")
      ?.toString();
    const ps_number: string | undefined = formData.get("ps_number")?.toString();
    if (typeof ps_id === "undefined") {
      message = "KO";
      return error(400, {
        message: "Something went wrong...",
      });
    }
    let output = db.editParkingSite(ps_id, ps_description, ps_number);
    console.log(output);
    // const parkingSites = await db.getAllTParkingSites();
    console.log("from doAction" + message);
    return { message: message };
  },
  delete: async ({ request }) => {
    const formData = await request.formData();
    const ps_id: string | undefined = formData.get("ps_id")?.toString();
    message = "OK";
    if (typeof ps_id === "undefined") {
      message = "KO";
      return error(400, {
        message: "Something went wrong...",
      });
    }
    db.deleteParkinSite(ps_id);
    //const parkingSites = await db.getAllTParkingSites();
    return { message: message };
  },
};
