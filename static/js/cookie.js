const csrftoken = getCsrfToken('csrftoken');
console.log("csrf-Token", csrftoken);

let shopping_card = JSON.parse(getShoppingCartCookie('shopping_card'));
console.log('Warenkorb 1:', shopping_card);

if (shopping_card == undefined) {
  shopping_card = {};
  document.cookie = "shopping_card=" + JSON.stringify(shopping_card) + ";path=/; SameSite=None; Secure"; /** "domain;path=/" ->cookie is valid for entire website*/
  console.log('Warenkorb 2:', shopping_card);
}

/**
 * get csrf token
 * @param {*} name 
 * @returns 
 */
function getCsrfToken(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(
          cookie.substring(name.length + 1)
        );
        break;
      }
    }
  } else {
    cookieValue = "0815"
  }
  return cookieValue;
}


/**
 * get shopping card cookie
 * @param {*} name 
 * @returns 
 */
function getShoppingCartCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(
          cookie.substring(name.length + 1)
        );
        break;
      }
    }
  } else {
    cookieValue = {}
  }
  return cookieValue;
}



