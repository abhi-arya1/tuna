import { Project, User } from "@/lib/dtypes";
import { createClient } from "../client";
import authenticate from "./utils-client";
import { fetchUserById } from "./users";

const context = createClient();

export async function fetchUserProjects() {
  const user = await authenticate();

  const { data: projectsData, error: projectsError } = await context
    .from("projects")
    .select("*")
    .eq("creator_id", user?.id)

  if (projectsError) {
    console.error("Error fetching projects data:", projectsError.message);
    throw projectsError;
  }

  return projectsData; 
}


export async function fetchProjectById(projectId: string): Promise<Project> {
  // await authenticate();

  const { data, error } = await context
    .from("projects")
    .select("*")
    .eq("id", projectId)
    .single();

  if (error) {
    console.error("Error fetching project:", error.message);
    throw error;
  }
  return data;
}

export async function createProject(
  name: string,
  userData: User,
  chatHistory?: any[],
) {
  const { data, error } = await context
    .from("projects")
    .insert([
      {
        creator_id: userData?.id,
        name: name,
        chat_history: (chatHistory || []),
      },
    ])
    .select('id');

  // console.log(data);
  return data;
}



export async function updateProject(projectId: string, updateData: Record<string, any>) {
  // const user = await authenticate();

  const { data, error } = await context
    .from("projects")
    .update(updateData)
    .eq("id", projectId)
    .select('*')
    .single();

  if (error) {
    console.error("Error updating user:", error.message);
    throw error;
  }

  // console.log("Update successful, returned data:", data);
  return data;
}



export async function updateChatHistory(
  projectId: string,
  chatHistory: any[]
) {
  const { data, error } = await context
    .from("projects")
    .update({ chat_history: chatHistory })
    .eq("id", projectId)
    .select('*')
    .single();

  if (error) {
    console.error("Error updating chat history:", error.message);
    throw error;
  }

  // console.log(data);

  return data;
}

export async function deleteProject(projectId: string) {
  const user = await authenticate();

  const { error } = await context.from("projects").delete().eq("id", projectId);

  if (error) {
    console.error("Error deleting project:", error.message);
    throw error;
  }
}
