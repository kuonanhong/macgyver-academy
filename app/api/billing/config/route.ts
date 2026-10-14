import { json } from "@/lib/backend";
export const dynamic = "force-dynamic";
/** Sites is the full owner/demo edition. Static assets are not a paywall. */
export async function GET() {
  return json({
    mode: "disabled", protected: false, checkoutAvailable: false,
    freeCourseIds: ["semiconductor", "packaging", "a201", "a242", "a271", "a281"],
    plans: [
      { id: "all-30", title: "全學院 30 天", titleEn: "Academy · 30 days", amountTwd: 299, durationDays: 30 },
      { id: "all-365", title: "全學院 365 天", titleEn: "Academy · 365 days", amountTwd: 2490, durationDays: 365 },
    ],
    termsVersion: "v10-2026-10", termsUrl: "commerce-terms.html",
    legalUrls: { terms: "commerce-terms.html", privacy: "commerce-terms.html#privacy", refund: "commerce-terms.html#refund" },
    certificateType: "local-learning-statement",
    reason: "The Sites owner/demo edition contains the complete curriculum. Paid checkout requires the separately configured protected HTTPS server; no card payment is enabled here.",
  });
}
