
let orderOrDeleteButtons = document.querySelectorAll('.btn-add-or-delete');
let cardCounter = document.getElementById('card-counter');


orderOrDeleteButtons.forEach(button => {
  button.addEventListener('click', (e) => {
    e.preventDefault();
    let articleId = e.target.getAttribute('data-article');
    let action = e.target.getAttribute('data-action');

    console.log('Benutzer:', current_user);
    if (current_user == 'AnonymousUser') {
      updateGuestOrder(articleId, action);
    } else {
      updateOrder(articleId, action)
    }

  });
});

function updateGuestOrder(articleId, action) {
  // console.log(articleId, action);
  if (action == 'addToShoppingCart') {
    if (shopping_card[articleId] == undefined) {
      shopping_card[articleId] = { 'quantity': 1 };
      console.log("ShoppingCard", shopping_card);
    } else {
      shopping_card[articleId]['quantity'] += 1;
    }
  }
  if (action == 'removeFromShoppingCart') {
    shopping_card[articleId]['quantity'] -= 1;
    if (shopping_card[articleId]['quantity'] <= 0) {
      delete shopping_card[articleId];
    }
  }

  document.cookie = "shopping_card=" + JSON.stringify(shopping_card) + ";path=/; SameSite=None; Secure";
  console.log("ShoppingCard", shopping_card);
  location.reload();
}


function updateOrder(articleId, action) {
  let url = '/article_backend/';

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


// Checkout

current_URL = window.location.href.split('/').at(-2);

if (current_URL === 'kasse') {
  let checkoutForm = document.getElementById('form-checkout');
  let total_price = (document.getElementById('hidden-total-price').value) * 1;
  checkoutForm.addEventListener('submit', (e) => {
    e.preventDefault();
    document.getElementById('form-forward-button').classList.add('d-none');
    document.getElementById('info-checkout').classList.add('show');
  });

  document.getElementById('form-checkout-button').addEventListener('click', (e) => {
    submitForm(total_price, checkoutForm)
  });
}


function submitForm(total_price, checkoutForm) {
  let userData = {
    'name': checkoutForm.inputName.value,
    'email': checkoutForm.inputEmail.value,
    'total_price': total_price
  }

  let invoiceData = {
    'address': checkoutForm.inputAddress.value,
    'plz': checkoutForm.inputPlz.value,
    'city': checkoutForm.inputCity.value,
    'bundesland': checkoutForm.inputState.value,
  }

  let url = '/order_backend/';

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    },
    body: JSON.stringify({
      'user_data': userData,
      'invoice_data': invoiceData
    })
  }
  )
    .then(() => window.location.href = '/')
}
