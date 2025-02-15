"use client"; 

import { User } from '@/lib/dtypes';
import { createClient } from '@/lib/supabase/client';
import { fetchUserById } from '@/lib/supabase/db/users';
import { Session } from '@supabase/supabase-js';
import { useEffect, useState, createContext, useContext } from 'react';

interface AuthContextType { 
    session: Session | null; 
    user: User | null; 
    setSession: (session: Session | null) => void;
    setUser: (user: User | null) => void;
    resetUser: () => void;
}

const defaultAuthContext: AuthContextType = {
    session: null, 
    user: null, 
    setSession: () => {},
    setUser: () => {},
    resetUser: () => {},
}

const supabase = createClient();
const AuthContext = createContext<AuthContextType>(defaultAuthContext);

export const AuthProvider = ({ children }: any) => {
  const [session, setSession] = useState<Session | null>(null);
  const [user, setUser] = useState<User | null>(null); 

  useEffect(() => {
    console.log(user);
  }, [])

  useEffect(() => {
    const initSession = async () => {
      const {
        data: { user },
      } = await supabase.auth.getUser();

        const userData = await fetchUserById("");
        setUser(userData);
    };

    initSession();

    const { data: authListener } = supabase.auth.onAuthStateChange(
      (event, _session) => {
        // console.log(event);
        // console.log("User Event: ", event, "Session User ID", _session?.user?.id);

        if (localStorage.getItem('opennote-session')) {
          const sesh: Session = JSON.parse(localStorage.getItem('opennote-session') || '')
          // console.log("Retrieving session from local storage", sesh.user.id);

          supabase.auth.setSession(sesh);

          setSession(sesh);
          if (_session?.user) {
            fetchUserById(_session.user.id).then((userData: any) => {
              setUser(userData);
              localStorage.removeItem('opennote-session');
            });
          }
          return;
        }
        

        if (event === "SIGNED_IN"
            || event === "USER_UPDATED"
            || event === "INITIAL_SESSION" 
            || event === "TOKEN_REFRESHED"
        ) {
          setSession(_session);
          fetchUserById("").then((userData: any) => {
            setUser(userData);
          });
        } else {
          setSession(null);
          setUser(null);
        }
      }
    );

    return () => {
      authListener?.subscription.unsubscribe();
    };
  }, []);

  const handleSetSession = (session: Session | null) => {
    setSession(session);
  }

  const handleSetUser = (user: User | null) => {
    setUser(user);
  }


  const resetUser = async () => {
    const user = await fetchUserById("")
    setUser(user);
    // console.log(user);
  }

  return (
    <AuthContext.Provider 
        value={{
            session, 
            user,
            setSession: handleSetSession,
            setUser: handleSetUser,
            resetUser,
        }}
    >
        {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
