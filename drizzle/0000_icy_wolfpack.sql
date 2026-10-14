CREATE TABLE `ai_rate_limits` (
	`user_id` text NOT NULL,
	`window` integer NOT NULL,
	`count` integer DEFAULT 0 NOT NULL,
	PRIMARY KEY(`user_id`, `window`)
);
--> statement-breakpoint
CREATE TABLE `project_progress` (
	`user_id` text NOT NULL,
	`project_id` text NOT NULL,
	`completed` text DEFAULT '[]' NOT NULL,
	`notes` text DEFAULT '' NOT NULL,
	`assembly` text DEFAULT '[]' NOT NULL,
	`updated_at` integer NOT NULL,
	PRIMARY KEY(`user_id`, `project_id`)
);
