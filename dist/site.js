// Only load each archive video when a reader opens that report.
document.querySelectorAll('details.clip').forEach((details) => {
  details.addEventListener('toggle', () => {
    const slot = details.querySelector('.video-slot');
    if (!details.open || slot.querySelector('iframe')) return;
    const frame = document.createElement('iframe');
    frame.className = 'video';
    frame.src = slot.dataset.src;
    frame.title = slot.dataset.title;
    frame.allow = 'encrypted-media; picture-in-picture; fullscreen';
    frame.referrerPolicy = 'strict-origin-when-cross-origin';
    frame.allowFullscreen = true;
    slot.append(frame);
  });
});
