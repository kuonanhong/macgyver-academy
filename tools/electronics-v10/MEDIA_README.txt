V10 media supplement, reviewed 2026-10-14

Integrate tools/electronics-v10/media.json after V9. Merge photos by ID,
sources by ID, courses by courseId, guides by guide ID, and videos by
YouTube ID (to avoid duplicate cards when an existing course has the same
background video). Preserve previous media. Photo associations also include
relevant V10 electrical/electronics courses; these do not require extra video
cards. Append the new source IDs used by each course where the application's
source-library reverse index expects course.sourceIds.

31 new real raster assets: material specimens, instrumentation, assemblies,
microscopy and one radiograph. Two photographed/drawn diagrams discovered
during research were deliberately excluded from the photo count. License
families are CC BY, CC BY-SA, CC0 or explicit public-domain dedication.
Every asset records creator, source, license link, changes, scope and SHA256.
V10-LICENSES.txt preserves redistribution credits. A stock/product photo is
not evidence of the current course's exact manufacturer or process.

All 199 semiconductor/packaging topics receive a distinct bilingual visual
observation workbook. The booklets reuse the academy's original sourced
course principles while adding an explicit image/evidence comparison task.
Each has a Chinese and English original SVG learning map (398 files, 199
subjects, eight inquiry-family symbols). These map course units to model,
observation, discrimination and acceptance; they are not manufacturer's
physical cross-sections, process recipes or dimensioned drawings.

Seven newly verified official YouTube videos, plus two existing ASML
background videos, are distributed by technical context. A video is shared
where relevant and is explicitly labeled as supporting background, not
unique footage of each lesson/step. No video is downloaded, clipped,
transcribed, rehosted, or claimed to have been watched end to end. The
bilingual key points are independently authored from the official linked
video descriptions and technical pages. oEmbed proves a title/channel/player
response, not successful playback in every region or browser; runtime
fallback links remain necessary. Caption availability is provider-controlled.

Browser UI can select diagram.path or diagram.pathEn and all paired *En
text fields. Other languages use the application's configured translation
service; these assets do not assert professionally reviewed 79-language
coverage. An SVG image's embedded text is only Chinese or English.

Rebuild: python tools/electronics-v10/build_media.py
Verify: python tools/electronics-v10/test_media.py
The builder is network-free, using stable V9 course and source snapshots,
verified video oEmbed records and attribution-only photo metadata. The
optional research/download scripts are authoring utilities, never required
by a learner or production runtime. They may hit provider rate limits.
