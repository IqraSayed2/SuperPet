function updateQuantity(productid, operation) {

  const inputBox = document.getElementById("quantity" + productid);
  inputBox.value = parseInt(inputBox.value) + operation;
  if (inputBox.value < 1) 
   inputBox.value = 1;

}
