// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
type User = {
  id: number;
  email: string;
  role: string;
};
declare global {
  namespace App {
    interface Locals {
      user: User | null;
      something: String | null;
    }
    // interface Error {}
    // interface Locals {}
    // interface PageData {}
    // interface PageState {}
    // interface Platform {}
  }
}

// Define an interface for the structure of each infraction
// Define the infractionsStore with the specified type

export { };
