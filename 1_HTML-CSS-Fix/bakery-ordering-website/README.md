# Sweet Crumbs Bakery Website

## Overview
This project is a responsive website for a mid-level bakery that allows customers to browse the menu, place orders, and book tables. The menu data is stored in a JSON file, while orders and bookings are captured dynamically in the JavaScript code.

## Features
- **Dynamic Menu**: All items are loaded from `menu.json`, making it easy to update or expand the menu.
- **Order Form**: Users can select menu items, specify quantity, and submit orders.
- **Booking Form**: Users can book tables by providing their name, date, and number of guests.
- **Responsive Design**: The layout adapts to different screen sizes for a smooth user experience.
- **Developer Notes**: JS comments are included to help understand code structure and functionality.


## How It Works
1. The menu is loaded dynamically from `data/menu.json` using JavaScript.
2. Orders submitted via the form are stored in a local array (`orders`) in the browser.
3. Bookings submitted via the form are stored in a local array (`bookings`) in the browser.
4. Console logs can be used to review all orders and bookings captured during the session.

## Notes
- This project simulates a working bakery system without requiring a backend.
- The structure is modular, allowing future integration with real server storage or databases.
- Designed to demonstrate front-end development skills using HTML, CSS, JavaScript, and JSON.
