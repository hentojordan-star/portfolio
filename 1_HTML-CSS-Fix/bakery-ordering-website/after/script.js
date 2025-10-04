// Arrays to store orders and bookings
let orders = [];
let bookings = [];

// Load menu JSON
fetch('data/menu.json')
  .then(response => response.json())
  .then(menuData => {
    const menuContainer = document.getElementById('menuContainer');
    const orderSelect = document.getElementById('orderItem');

    menuData.forEach(category => {
      const catDiv = document.createElement('div');
      const catTitle = document.createElement('h3');
      catTitle.textContent = category.category;
      catDiv.appendChild(catTitle);

      category.items.forEach(item => {
        const itemDiv = document.createElement('div');
        itemDiv.className = 'menu-item';
        itemDiv.innerHTML = `<strong>${item.name}</strong><br>Price: $${item.price}`;
        catDiv.appendChild(itemDiv);

        // Add item to order dropdown
        const option = document.createElement('option');
        option.value = item.name;
        option.textContent = item.name;
        orderSelect.appendChild(option);
      });

      menuContainer.appendChild(catDiv);
    });
  })
  .catch(err => console.error('Error loading menu:', err));

// Handle orders
document.getElementById('orderForm').addEventListener('submit', function(e){
  e.preventDefault();
  const order = {
    name: document.getElementById('orderName').value,
    item: document.getElementById('orderItem').value,
    quantity: document.getElementById('orderQuantity').value
  };
  orders.push(order);
  alert('Order captured!');
  console.log(orders);
  this.reset();
});

// Handle bookings
document.getElementById('bookingForm').addEventListener('submit', function(e){
  e.preventDefault();
  const booking = {
    name: document.getElementById('bookingName').value,
    date: document.getElementById('bookingDate').value,
    guests: document.getElementById('bookingGuests').value
  };
  bookings.push(booking);
  alert('Booking captured!');
  console.log(bookings);
  this.reset();
});
    
