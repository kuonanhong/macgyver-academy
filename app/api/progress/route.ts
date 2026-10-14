import { and, eq } from "drizzle-orm";
import { getDb } from "@/db";
import { progress } from "@/db/schema";
import { body, boundedText, failure, HttpError, ids, json, userRequired } from "@/lib/backend";
export const dynamic = "force-dynamic";
export async function GET() {
  try {
    const user = await userRequired();
    const rows = await getDb().select().from(progress).where(eq(progress.userId, user.userId)).limit(2000);
    return json({ projects: Object.fromEntries(rows.map(r => [r.projectId, { completed: r.completed, notes: r.notes, assembly: r.assembly, updatedAt: r.updatedAt }])) });
  } catch (e) { return failure(e); }
}
export async function PUT(request: Request) {
  try {
    const user = await userRequired();
    const payload = await body(request);
    const projectId = boundedText(payload.projectId, "projectId", 100);
    if (!/^[a-zA-Z0-9_-]+$/.test(projectId)) throw new HttpError(400, "Invalid projectId.");
    const base = payload.baseUpdatedAt ?? null;
    if (base !== null && (typeof base !== "number" || !Number.isSafeInteger(base) || base < 0)) throw new HttpError(400, "Invalid baseUpdatedAt.");
    const db = getDb();
    const owned = and(eq(progress.userId, user.userId), eq(progress.projectId, projectId));
    const currentRow = async () => (await db.select().from(progress).where(owned).limit(1))[0];
    const conflict = async () => {
      const row = await currentRow();
      return json({ error: "Progress changed on another device", current: row ? { completed: row.completed, assembly: row.assembly, notes: row.notes, updatedAt: row.updatedAt } : null }, 409);
    };
    const current = await currentRow();
    if ((current && base !== current.updatedAt) || (!current && base !== null)) return conflict();
    const saved = { completed: ids(payload.completed, "completed"), assembly: ids(payload.assembly, "assembly"), notes: boundedText(payload.notes, "notes", 20_000, true), updatedAt: Math.max(Date.now(), (current?.updatedAt ?? 0) + 1) };
    if (current) {
      const changed = await db.update(progress).set(saved).where(and(owned, eq(progress.updatedAt, current.updatedAt))).returning({ projectId: progress.projectId });
      if (!changed.length) return conflict();
    } else {
      const inserted = await db.insert(progress).values({ userId: user.userId, projectId, ...saved }).onConflictDoNothing().returning({ projectId: progress.projectId });
      if (!inserted.length) return conflict();
    }
    return json({ projectId, ...saved });
  } catch (e) { return failure(e); }
}
