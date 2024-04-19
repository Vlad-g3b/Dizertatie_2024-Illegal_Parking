import * as db from "$lib/Utils";
import { error } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";
export const load: PageServerLoad = async ({}) => {
  const stats = await db.getStats();
  console.log(stats);
  return { stats };
};
