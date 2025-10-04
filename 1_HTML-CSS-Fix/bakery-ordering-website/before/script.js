// Orders form
document.getElementById("submit").addEventListener("click", function(e){
  e.preventDefault();
  var name = document.getElementById("orderName").value; // TODO: fix ID mismatch
  var item = document.getElementById("orderItem").value;
  var qty = document.getElementsByName("amount")[0].value;
  alert("Order received for " + item + " x" + qty); // Placeholder for actual submission
});

// Booking form
document.getElementById("submit").addEventListener("click", function(e){
  e.preventDefault();
  var name = document.getElementsByName("name")[0].value;
  var date = document.getElementsByName("date")[0].value;
  var guests = document.getElementsByName("guests")[0].value;
  alert("Booking requested for " + guests + " guests on " + date); // Placeholder
});

// TODO:
// - Duplicate IDs for buttons need fixing
// - Connect forms to backend or JSON storage
