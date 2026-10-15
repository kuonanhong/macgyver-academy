import { json } from "@/lib/backend";
export const dynamic = "force-dynamic";
/** Sites is the full owner/demo edition. Static assets are not a paywall. */
export async function GET() {
  return json({
    mode: "disabled", protected: false, checkoutAvailable: false,
    // V13: no whole course is free; only the first section (stage) of every guided course.
    freeCourseIds: [], freeStagesPerCourse: 1,
    plans: [
      { id: "all-30", title: "30 天學習通行證", titleEn: "30-day learning pass", amountTwd: 299, durationDays: 30 },
      { id: "all-365", title: "365 天學習通行證", titleEn: "365-day learning pass", amountTwd: 2490, durationDays: 365 },
    ],
    termsVersion: "v10-2026-10", termsUrl: "commerce-terms.html",
    legalUrls: { terms: "commerce-terms.html", privacy: "commerce-terms.html#privacy", refund: "commerce-terms.html#refund" },
    certificateType: "local-learning-statement",
    reason: "The Sites owner/demo edition contains the complete curriculum. Paid checkout requires the separately configured protected HTTPS server; no card payment is enabled here.",
  });
}
