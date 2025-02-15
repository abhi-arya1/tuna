"use server";

import { createClient } from "../server";

const context = createClient();

export default async function authenticate() {
    try {
        const { data, error } = await context.auth.getSession();
        if (error) { 
            console.log(error.message);
            throw new Error("Error getting session: " + error.message);
        }

        if (!data) {
            console.log("User is not logged in");
            throw new Error("Not authenticated.");
        }

        return data.session?.user;
    } catch (e) {
        console.error("Error authenticating:", e);
        throw e;
    };
}