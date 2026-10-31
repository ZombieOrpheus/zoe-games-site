'use strict';
const isStaging = /(?:^|\/)staging(?:\/|$)/.test(location.pathname);
if (isStaging) {
  document.getElementById('staging-banner').hidden = false;
  document.title = '[STAGING] ' + document.title;
  const robots = document.createElement('meta');
  robots.name = 'robots'; robots.content = 'noindex, nofollow'; document.head.append(robots);
}
document.getElementById('year').textContent = new Date().getFullYear();
document.getElementById('game-tools').hidden = false;
const cards = [...document.querySelectorAll('.game-card')];
const buttons = [...document.querySelectorAll('[data-filter]')];
const search = document.getElementById('search');
let filter = 'all';
function updateGames() {
  const query = search.value.trim().toLocaleLowerCase();
  let visible = 0;
  cards.forEach(card => {
    card.hidden = (filter !== 'all' && card.dataset.status !== filter) || !card.textContent.toLocaleLowerCase().includes(query);
    if (!card.hidden) visible++;
  });
  document.getElementById('no-results').hidden = visible !== 0;
}
buttons.forEach(button => button.addEventListener('click', () => {
  filter = button.dataset.filter;
  buttons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
  updateGames();
}));
search.addEventListener('input', updateGames);
