import * as db from "$lib/Utils";
import { error, redirect } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";
import { goto } from "$app/navigation";
let message: any = "";

export const load: PageServerLoad = async ({ locals }) => {
  const unresolvedTf = await db.getAllUnresolvedTrafficViolation();
  const latestNews = JSON.parse(unresolvedTf).TrafficViolationList.slice(0, 3);
  const users = await db.getUsersFrom();
  const session = await locals.auth();

  let latestNotes = await db.getAllNotes(session?.user?.name);
  latestNotes = JSON.parse(latestNotes)?.slice(0, 1)[0];
  return { latestNews, users, latestNotes };
};

export const actions = {
  viewNotes: async ({ locals, request }) => {
    goto("notes");
  },
  insert: async ({ locals, request }) => {
    message = "OK";
    const session = await locals.auth();

    db.insertNote(session?.user?.name);
    return { message: message };
  },
};
