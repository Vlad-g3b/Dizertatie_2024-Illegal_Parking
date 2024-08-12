import * as db from "$lib/Utils";
import { error } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";
export const load: PageServerLoad = async ({ locals }) => {
  const unresolvedTf = await db.getAllUnresolvedTrafficViolation();
  return { unresolvedTf };
};

export const actions = {
  resolveTf: async ({ request, locals }) => {
    const formData = await request.formData();
    const session = await locals.auth();
    const tf_id: string | undefined = formData.get("id")?.toString();
    if (typeof tf_id === "undefined") {
      return error(400, {
        message: "Something went wrong...",
      });
    }
    const dbOut = db.doUpdateResolved(tf_id, session?.user?.name);
    const unresolvedTf = await db.getAllUnresolvedTrafficViolation();
    return { unresolvedTf };
  },
};
