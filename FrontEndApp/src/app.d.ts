// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
import type { Session as AuthSession } from "@auth/core/types";

import { type AdapterUser, type User } from "@auth/sveltekit";

declare module "@auth/sveltekit" {
  interface User extends AdapterUser {
    role: string;
  }
}

declare global {
  namespace App {
    interface Locals {}
    interface Session extends AuthSession {}

    // interface Error {}
    // interface Locals {}
    // interface PageData {}
    // interface PageState {}
    // interface Platform {}
  }
}

export {};
// Define an interface for the structure of each infraction
