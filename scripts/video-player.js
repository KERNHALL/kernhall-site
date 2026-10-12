'use strict';

document.querySelectorAll('[data-youtube-id]').forEach(player => {
  const videoId = player.dataset.youtubeId;
  const button = player.querySelector('.video-load');
  if (!/^[A-Za-z0-9_-]{11}$/.test(videoId) || !button) return;

  button.hidden = false;
  button.addEventListener('click', () => {
    const iframe = document.createElement('iframe');
    iframe.src = `https://www.youtube-nocookie.com/embed/${videoId}?playsinline=1`;
    iframe.title = 'KERNHALL – HEIMKEHR | Vollständiges Musikvideo';
    iframe.allow = 'encrypted-media; picture-in-picture; fullscreen';
    iframe.allowFullscreen = true;
    iframe.referrerPolicy = 'strict-origin-when-cross-origin';
    player.replaceChildren(iframe);
    iframe.focus();
  }, { once: true });
});
