console.log('Current user:', current_user);

let orderOrDeleteButtons = document.querySelectorAll('.btn-add-or-delete');

let cardCounter = document.getElementById('card-counter');
let articleCounter = 0;


orderOrDeleteButtons.forEach(button => {
  button.addEventListener('click', (e) => {
    e.preventDefault();
    let articleId = e.target.getAttribute('data-article');
    let action = e.target.getAttribute('data-action');
    console.log(e.target);
    console.log('Article ID:', articleId);
    console.log('Action:', action);
    updateOrder(articleId, action);
  });
});

function updateOrder(articleId, action) {
  let url = '/article_backend/';
  console.log('csrf token:', csrftoken);

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    },
    body: JSON.stringify({
      articleID: articleId,
      action: action
    })
  }
  )
    .then(() => location.reload())
}


