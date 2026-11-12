(() => {
  const parts = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'Europe/Berlin', year: 'numeric', month: '2-digit', day: '2-digit'
  }).formatToParts(new Date());
  const values = Object.fromEntries(parts.map(part => [part.type, part.value]));
  const today = `${values.year}-${values.month}-${values.day}`;

  const content = document.getElementById('release-content');
  if (content) {
    if (today < content.dataset.releaseDate) {
      const robots = document.createElement('meta');
      robots.name = 'robots';
      robots.content = 'noindex';
      document.head.append(robots);
      return;
    }

    const metadata = document.getElementById('release-metadata');
    document.querySelector('head > title').remove();
    document.head.append(metadata.content);
    document.getElementById('release-placeholder').replaceWith(content.content);
  }

  document.querySelectorAll('template[data-release-date]').forEach(template => {
    if (template.dataset.releaseDate <= today) {
      template.replaceWith(template.content);
    }
  });

  const spotify = document.getElementById('song-spotify');
  const status = document.getElementById('song-status');
  if (!spotify || !status) return;
  const available = spotify.dataset.releaseDate <= today;
  spotify.hidden = !available;
  status.textContent = available
    ? 'Veröffentlicht / Released · Jetzt über die offiziellen Links anhören.'
    : 'Geplanter Release / Upcoming release · Über HyperFollow vormerken.';
})();
