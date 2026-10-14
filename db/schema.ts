import { integer, primaryKey, sqliteTable, text } from "drizzle-orm/sqlite-core";

export const progress = sqliteTable("project_progress", {
  userId: text("user_id").notNull(),
  projectId: text("project_id").notNull(),
  completed: text("completed", { mode: "json" }).$type<string[]>().notNull().default([]),
  notes: text("notes").notNull().default(""),
  assembly: text("assembly", { mode: "json" }).$type<string[]>().notNull().default([]),
  updatedAt: integer("updated_at").notNull(),
}, (t) => [primaryKey({ columns: [t.userId, t.projectId] })]);

export const aiRateLimits = sqliteTable("ai_rate_limits", {
  userId: text("user_id").notNull(),
  window: integer("window").notNull(),
  count: integer("count").notNull().default(0),
}, (t) => [primaryKey({ columns: [t.userId, t.window] })]);
