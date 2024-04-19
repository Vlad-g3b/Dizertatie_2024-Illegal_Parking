import * as db from "$lib/Utils";
import { error } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";
export const load: PageServerLoad = async ({ }) => {
  const trafficViolations = await db.getAllTrafficViolation();
  return { trafficViolations };
};

export const actions = {
  resolveTf: async ({ request }) => {
    const formData = await request.formData();
    console.log(formData);
    const tf_id: string | undefined = formData.get("id")?.toString();
    console.log(tf_id);
    if (typeof tf_id === "undefined") {
      return error(400, {
        message: "Something went wrong...",
      });
    }
    const dbOut = db.doUpdateResolved(tf_id);
    const trafficViolations = await db.getAllTrafficViolation();
    return { trafficViolations };
  },
};
