import { aiRoutes, body, boundedText, completion, hostedGemini, enforceAiLimit, failure, HttpError, json, TUTOR_POLICY, userRequired } from "@/lib/backend";
import { validateTutorImage, tutorHistory } from '@/lib/tutor-providers';
export const dynamic = "force-dynamic";
export async function POST(request: Request) {
  try {
    const user = await userRequired();
    const payload = await body(request, 6*1024*1024);
    const question = boundedText(payload.question, "question", 3000);
    const context = boundedText(payload.context ?? "", "context", 18000, true);
    const language = boundedText(payload.language ?? "zh-TW", "language", 50);
    const routes=aiRoutes();
    const route=routes.find(r=>r.id===(payload.route ?? routes[0]?.id));
    if(!route) throw new HttpError(503, 'This AI route is not configured.');
    if(payload.cloudConsent!==true) throw new HttpError(400, 'Confirm sending this question, context, history and optional image to the AI provider.');
    let image,history;
    try {image=validateTutorImage(payload.image);history=tutorHistory(payload.history);} catch(e) {throw new HttpError(400, (e as Error).message);}
    if(image && !route.supportsImages)throw new HttpError(400, 'This route accepts text only. Select a vision route.');
    await enforceAiLimit(user.userId);
    const prompt=JSON.stringify({language,question,reference_context:context,conversation_history:history});
    const result = route.id==='gemini'?await hostedGemini(TUTOR_POLICY,prompt,image):await completion(TUTOR_POLICY,prompt);
    return json({ ...result, generated: true, route:route.id });
  } catch (e) { return failure(e); }
}
