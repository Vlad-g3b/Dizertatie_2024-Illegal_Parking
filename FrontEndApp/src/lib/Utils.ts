import { VITE_API_SERVER_URL } from "$env/static/private";

export async function getUserFromDbByEmail(email: string | null | undefined) {
  console.log("USER from DB " + email);
  try {
    const res = await fetch(VITE_API_SERVER_URL + "/getUser", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        usr_email: email,
      }),
    });
    return await res;
  } catch (error) {
    console.error(error);
  }
  return null;
}
export async function createUserProfile(
  profile: import("@auth/sveltekit").Profile | undefined
) {
  try {
    const res = await fetch(VITE_API_SERVER_URL + "/insertUser", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        usr_email: profile?.email,
        usr_name: profile?.name,
      }),
    });
    return await res;
  } catch (error) {
    console.error(error);
  }
  return null;
}

export async function doUpdateResolved(id: string | undefined) {
  let data: { tf_id: any; tf_type: string; is_resolved: number } = {
    tf_id: id,
    tf_type: "TrafficViolation",
    is_resolved: 1,
  };
  const res = await fetch(VITE_API_SERVER_URL + "/updateResolved", {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    throw new Error("Request failed");
  }
  return await res;
}

export async function getAllTrafficViolation() {
  try {
    const res = await fetch(VITE_API_SERVER_URL + "/getAllTrafficViolation");
    if (res.ok) {
      const data = await res.json();
      return data;
    } else {
      throw new Error("Request failed");
    }
  } catch (error) {
    console.error("Error fetching data:", error);
  }
}

export async function getAllTParkingSites() {
  const res = await fetch(VITE_API_SERVER_URL + "/getAllTParkingSites");
  if (res.ok) {
    return await res.json();
  } else {
    // Sometimes the API will fail!
    throw new Error("Request failed");
  }
}

export async function getStats() {
  const res = await fetch(VITE_API_SERVER_URL + "/getStats");
  if (res.ok) {
    return await res.text();
  } else {
    // Sometimes the API will fail!
    throw new Error("Request failed");
  }
}

export async function getAllUnresolvedTrafficViolation() {
  const res = await fetch(
    VITE_API_SERVER_URL + "/getAllUnresolvedTrafficViolation"
  );
  if (res.ok) {
    return await res.text();
  } else {
    // Sometimes the API will fail!
    throw new Error("Request failed");
  }
}
