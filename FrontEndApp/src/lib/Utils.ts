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

export async function getUsersFrom() {
  try {
    const res = await fetch(VITE_API_SERVER_URL + "/getUsers", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    return await res.json();
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
        usr_profile_pic: profile?.picture,
      }),
    });
    return await res;
  } catch (error) {
    console.error(error);
  }
  return null;
}

export async function insertOrUpdatePolygon(
  id: number,
  ps_id: string | undefined,
  cm_polygon: string | undefined,
  username: undefined | string | null
) {
  try {
    const res = await fetch(VITE_API_SERVER_URL + "/insertOrUpdatePolygon", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        cm_id: id,
        cm_ps_id: ps_id,
        cm_polygon: cm_polygon,
      }),
    });
    console.log("User " + username + " inserted " + cm_polygon);
    return await res;
  } catch (error) {
    console.error(error);
  }
  return null;
}

export async function doUpdateResolved(
  id: string | undefined,
  username: string | null | undefined
) {
  let data: {
    tf_id: any;
    tf_type: string;
    is_resolved: number;
    username: string | undefined | null;
  } = {
    tf_id: id,
    tf_type: "TrafficViolation",
    is_resolved: 1,
    username: username,
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

export async function getPolygon(cm_id: number) {
  try {
    const res = await fetch(VITE_API_SERVER_URL + "/getPolygon", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        cm_id: cm_id,
      }),
    });
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

export async function getAllPolygons() {
  try {
    const res = await fetch(VITE_API_SERVER_URL + "/getAllPolygons");
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

export async function editParkingSite(
  ps_id: any,
  ps_description: any,
  ps_number: any
) {
  const res = await fetch(VITE_API_SERVER_URL + "/editParkingSite", {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      ps_id: ps_id,
      ps_description: ps_description,
      ps_max_parking_spots: ps_number,
    }),
  });
  if (res.ok) {
    return await res.json();
  } else {
    // Sometimes the API will fail!
    throw new Error("Request failed");
  }
}

export async function deleteParkinSite(ps_id: any) {
  const res = await fetch(VITE_API_SERVER_URL + "/deleteParkingSite", {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      ps_id: ps_id,
    }),
  });
  if (res.ok) {
    return await res.json();
  } else {
    // Sometimes the API will fail!
    throw new Error("Request failed");
  }
}
