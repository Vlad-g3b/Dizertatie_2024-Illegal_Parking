import * as db from "$lib/Utils";
import { error } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";
let message: any = "";

export const load: PageServerLoad = async ({}) => {
  const logs = await db.getLogs();
  return { logs };
};
