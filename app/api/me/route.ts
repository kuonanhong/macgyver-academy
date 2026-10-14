import { getChatGPTUser } from "@/app/chatgpt-auth";
import { aiAvailable, aiRoutes, failure, json } from "@/lib/backend";
export const dynamic = "force-dynamic";
export async function GET() {
  try {
    const user = await getChatGPTUser();
    return json({ user: user ? { id: user.userId, name: user.displayName, email: user.email } : null, aiAvailable: aiAvailable(), aiRoutes:aiRoutes(), authMode: "chatgpt" });
  } catch (e) { return failure(e); }
}
