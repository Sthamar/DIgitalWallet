import { writable } from "svelte/store";

export const username = writable("");
export const user_pin = writable("");
export const apiBaseUrl = "http://127.0.0.1:8000";
