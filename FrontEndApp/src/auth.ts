import { SvelteKitAuth } from "@auth/sveltekit";
import GitHub from "@auth/sveltekit/providers/github";
import { GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET } from "$env/static/private";
import { type User } from "$lib/interfaces/User";
import { getUserFromDbByEmail, createUserProfile } from "$lib/Utils";

export const { handle, signIn, signOut } = SvelteKitAuth({
  providers: [
    GitHub({ clientId: GITHUB_CLIENT_ID, clientSecret: GITHUB_CLIENT_SECRET }),
  ],
  callbacks: {
    async session({ session, token }) {
      session.user.role = token.role as string;
      console.log(session);
      return { ...session };
    },
    async signIn({ profile }) {
      console.log("User signed in: " + profile?.name);
      try {
        let res = await getUserFromDbByEmail(profile?.email);
        if (res?.status === 404) {
          try {
            await createUserProfile(profile);
          } catch (error) {
            console.error(error);
          }
        }
        let user: User = await res?.json();
        console.log(user);
        return true;
      } catch (error) {
        console.error("Error fetching user data:", error);
        return false;
      }
    },
    async jwt({ token }) {
      let res = await getUserFromDbByEmail(token.email);
      const myUser: User = await res?.json();
      token.role = myUser.usr_role;
      // console.log("FROM TOKEN", token);
      return token;
    },
  },
});
