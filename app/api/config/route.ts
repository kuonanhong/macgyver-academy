import { aiAvailable, aiRoutes, json } from '@/lib/backend';
export const dynamic='force-dynamic';
export async function GET() {return json({aiAvailable:aiAvailable(),translationAvailable:aiAvailable(),aiRoutes:aiRoutes(),imageLimitBytes:4194304,authMode:'chatgpt'});}
