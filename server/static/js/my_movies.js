const MOVIES_URL = '/my-movies';

const list = document.querySelector('.movies__list');

const deleteMovie = (imdb) => {
  fetch(`${MOVIES_URL}/${imdb}`, { method: 'DELETE' })
    .then(() => location.reload())
    .catch((error) => console.log(error));
};

const updateNote = (imdb, note, item) => {
  fetch(`${MOVIES_URL}/${imdb}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'text/json' },
    body: JSON.stringify({ note }),
  })
    .then(() => {
      item.classList.add('movies__item--active');
      setTimeout(
        () => void item.classList.remove('movies__item--active'),
        1500
      );
    })
    .catch((error) => console.log(error));
};

if (list) {
  list.addEventListener('click', ({ target }) => {
    const item = target.closest('li');
    const imdb = item.dataset.imdb;

    if (target.classList.contains('movies__delete')) {
      deleteMovie(imdb);
    } else if (target.classList.contains('movies__update')) {
      const note = target.closest('form').querySelector('.movies_note').value;
      updateNote(imdb, note, item);
    }
  });
}
