V9 advanced packaging / silicon photonics media

Deployable supplement: media.json
- 14 new licensed physical photographs/micrographs, 2,157,146 bytes total.
- 6 existing photo records extended by ID, preserving earlier course assignments.
- 100 primaryPhotos mappings, each with explicit courseContext and representative scope.
- 11 new verified YouTube IDs and 85 topic-specific video assignments.
- 100 original Traditional Chinese / English visual-verification worksheets (5 actions each).
- 8 primary-reference records. Full source prose is not copied.

Rights
Exact author, license, license URL, original Commons file page, download URL and SHA-256
are stored in each photo record and media-verification.json. The 14 new local images
are Wikimedia original/thumbnail copies, with no scene edits. Share-alike licenses
continue to apply to the corresponding images; the website does not claim ownership.
The original full images were visually inspected. Flip_chip.jpg was excluded because
it is an illustration, not a photograph. Quilt Packaging microscopy is explicitly
identified as such and is never labeled as CoWoS, EMIB or copper-pillar production.
Photos are representative context, not 100 different factories or an actual photograph
for every process step. Existing generic micrographs likewise retain provenance.

Video verification
On 2026-10-14, YouTube oEmbed returned exact title, author/channel and embed metadata
for all 11 IDs. PI's official video library and AIM's official news page provide
corroborating publisher links; the remaining publishers are identified in oEmbed.
No video bytes were downloaded or rehosted. Playback in a real browser was not tested.
YouTube can still require sign-in or block a region/embed/browser/network. Every video
has an external source fallback; every one of the 100 courses has a bundled reading
worksheet independent of YouTube. The application does not bypass access restrictions.
The Ozen Engineering entry is an instructor/publisher tutorial, not foundry SOP.
The CA DREAMS video is linked explicitly from AIM Photonics' official website.

Rebuild
python tools/packaging-v9/build_media.py
This authoring script uses bundled media-research metadata plus already-downloaded
local images. It does not need network, credentials, or the /tmp research cache.
Do not delete local photo assets before rebuilding. Regenerated metadata is merged
by the main V9 integrator; this builder does not modify public/academy/data directly.

Checks performed
All 20 referenced files decode as images. All 14 new SHA-256 digests match.
All 100 course IDs match category packaging. Each guide has Chinese/English titles,
concept, 5 procedures, evidence, pitfalls, scope and references. All video IDs match
YouTube's 11-character syntax, verified oEmbed true, playbackTested false.
