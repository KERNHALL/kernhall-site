(() => {
  const spotify = document.getElementById('song-spotify');
  const status = document.getElementById('song-status');
  if (!spotify || !status) return;
  const parts = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'Europe/Berlin', year: 'numeric', month: '2-digit', day: '2-digit'
  }).formatToParts(new Date());
  const values = Object.fromEntries(parts.map(part => [part.type, part.value]));
  const today = `${values.year}-${values.month}-${values.day}`;
  const available = spotify.dataset.releaseDate <= today;
  spotify.hidden = !available;
  status.textContent = available
    ? 'Veröffentlicht / Released · Jetzt über die offiziellen Links anhören.'
    : 'Geplanter Release / Upcoming release · Über HyperFollow vormerken.';
})();
