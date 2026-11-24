/* Optional published YouTube destinations. Empty values keep links hidden.
 * Fill only after the playlist / video has been created and verified.
 * videos: [{ tour: 'interposer', videoId: 'YOUTUBE_ID' }, ...]
 */
window.MACGYVER_PACKAGING_YOUTUBE = {
  playlistId: '',
  videos: [],
  longVideos: [] // {tour, videoId, status:"verified"} only after the longer film is published
};
