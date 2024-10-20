import * as db from "$lib/Utils";
import { error } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";
export const load: PageServerLoad = async ({ locals }) => {
  const unresolvedTf = await db.getAllUnresolvedTrafficViolation();
  const latestNews = JSON.parse(unresolvedTf).TrafficViolationList.slice(0, 3);
  const users = await db.getUsersFrom();
  console.log(users);
  return { latestNews, users };
};
