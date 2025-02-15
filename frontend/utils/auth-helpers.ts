'use server';

import { createClient } from "@/lib/supabase/server";
import { AuthError, OAuthResponse, SupabaseClient } from "@supabase/supabase-js";
import { redirect } from "next/navigation";
import { cache } from "react";

const DEFAULT_AVATAR = "https://static.vecteezy.com/system/resources/thumbnails/009/292/244/small/default-avatar-icon-of-social-media-user-vector.jpg"

export const getUser = cache(async () => {
    const supabase = createClient();
    const {
      data
    } = await supabase.auth.getUser();
    return (data as any).raw_user_meta_data;
  });

export async function signUpWithPassword(email: string, password: string, users_name: string): Promise<AuthError | null> { 
    const supabase = createClient();
    const { error } = await supabase.auth.signUp({
        email: email,
        password: password,
        options: {
          data: {
            email: email,
            name: users_name,
            avatar_url: DEFAULT_AVATAR
          },
        },
      });

    return error; 
}


export async function signInWithPassword(email: string, password: string): Promise<AuthError | null> { 
    const supabase = createClient();
    const { error } = await supabase.auth.signInWithPassword({
        email: email,
        password: password,
    });
    return error;
}

export async function signOut(): Promise<string> { 
    const supabase = createClient();
    const { error } = await supabase.auth.signOut();
    if (error) { 
        console.log(error)
        return '/';
    }
    // location.reload();
    return '/';
}
