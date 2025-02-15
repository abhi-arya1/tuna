

type User = {
    id: string;
    name: string;
    email: string;
    avatar_url: string;
    projects: string[];
}

type Project = {
    id: string; 
    created_at: string; 
    creator_id: string; 
    name: string; 
    chat_history: any[];
    metadata: any;
}

export type {
    User,
    Project
};