import { redirect, type Handle } from "@sveltejs/kit";
import { handle as authenticationHandle } from "./auth";
import { sequence } from "@sveltejs/kit/hooks";
import { error } from "@sveltejs/kit";

export const authorizationHandle: Handle = async ({ event, resolve }) => {
  console.log("Authorization Handle ...  ");
  const session = await event.locals.auth();
  if (event.url.pathname.startsWith("/admin")) {
    if (!session) {
      throw redirect(303, "/");
    }
    if (session?.user?.role != "admin") {
      return error(403, {
        message: "Access Denied!",
      });
    }
  }

  if (event.url.pathname.startsWith("/moderator")) {
    if (!session) {
      throw redirect(303, "/");
    }
    if (session?.user?.role != "moderator") {
      return error(403, {
        message: "Access Denied!",
      });
    }
  }

  if (event.url.pathname.startsWith("/user")) {
    if (!session) {
      // Redirect to the signin page
      //throw redirect(303, "/");
    }
  }
  const response = await resolve(event);
  //console.log(response);
  // If the request is still here, just proceed as normally
  return response;
};

// First handle authentication, then authorization
// Each function acts as a middleware, receiving the request handle
// And returning a handle which gets passed to the next function
export const handle: Handle = sequence(
  authenticationHandle,
  authorizationHandle
);
