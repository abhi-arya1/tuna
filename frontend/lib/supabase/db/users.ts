import { User } from "@/lib/dtypes";
import { createClient } from "../client";

const context = createClient();

export async function fetchUserById(id: string): Promise<User> {
    const { data, error } = await context
        .from("users")
        .select("*")
        .single();

    if (error) {
        console.error("Error fetching data:", error);
    }

    return data;
}