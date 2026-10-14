/* Public browser settings. Never put passwords, private tokens or AI keys here.
 * To use your own HTTPS deployment, edit only videoPlayerUrl below. Deploy the
 * included public-player/dist files at that URL with anonymous static access.
 * Keep the main academy's account data and access rules separate. The URL must
 * end in /video-player.html with no query or fragment.
 * googleMapsEmbedKey is an optional BROWSER key: restrict HTTP referrers and the
 * Maps Embed API in Google Cloud. It is visible to every site visitor, not secret.
 */
window.MG_CONFIG = Object.assign({
  videoPlayerUrl: 'https://macgyver-public-player.kuonanhong.chatgpt.site/video-player.html',
  googleMapsEmbedKey: '',
  // Optional cloud accounts: use only publishable / anon key after applying supabase SQL.
  siteMode: 'auto',
  supabaseUrl: '',
  supabasePublishableKey: '',
  // Runtime is bundled. GGUF weights download only after explicit learner consent.
  aiRuntimeBase: './vendor/wllama/',
  // BEGIN GENERATED YOUTUBE IDS — node tools/build-public-player.mjs
  allowedYouTubeIds: ["-egYoxajTz0","0rVQHFPZfJk","1nYQV88Jbcg","2ytGLTAGlwk","4G8wXQGEBrA","6UqW4GEla3Q","78Z5nkh_m-0","CAKWkOuoWrs","ClAgalrHyig","Fml3yuPR2AU","GFc_NIgC_E0","GlwtS_Vq9aE","HEyW9ox9Ne0","HydRZ0oXg2M","IhbQqEMlUz8","MfFGRl00LKY","NrahF3opykM","P7UDE2cISPQ","Rt-7c9Wgnds","ST_1krgYni4","Skdf8ekrHbU","UAWu1O1UuQc","VSX-tFSwCtE","W0jlu0ghNIg","XV-aIWEBTsg","YhbUOq5oaes","Z-E5IUozd7M","_5TSeXkX5Js","_T-mh72VRIY","_TG3lUu-k0k","blW-Fa4a10g","bor0qLifjz4","dpekP4lbAMw","dxlDqeF0IhM","e2DYwblIr-E","fCBlXMDpa2I","h_zgURwr6nA","haYFixYgrHM","hksKKrkcAJg","l6o7VH8lJk4","pPPiaGU12Og","pk7yLLw3zAU","rGhfF44-QsE","stvB1MPTF-c","t_YmVXB6veY","v9Pg92cdJa4","wJVDpclyG6A","ykfong1WNU8"],
  // END GENERATED YOUTUBE IDS
}, window.MG_CONFIG || {});
