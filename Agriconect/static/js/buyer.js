// Add active class to current navigation item
document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('.sidebar nav a');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // Notification bell click handler
    const notificationBell = document.querySelector('.fa-bell');
    notificationBell.addEventListener('click', function() {
        alert('Notifications feature coming soon!');
    });

    // Settings icon click handler
    const settingsIcon = document.querySelector('.fa-cog');
    settingsIcon.addEventListener('click', function() {
        alert('Settings feature coming soon!');
    });

    // Add hover effect to crop cards
    const cropCards = document.querySelectorAll('.crop-card');
    cropCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
            this.style.transition = 'all 0.3s ease';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'none';
        });
    });
});

document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('click', function() {
        const action = this.textContent;
        const productCard = this.closest('.product-card');
        const productName = productCard.querySelector('.product-name').textContent;
        console.log(`${action} clicked for ${productName}`);
    });
});

let cart = []; // Array to hold cart items
let totalAmount = 0; // Variable to hold total amount
let activeOrders = 0; // Variable to hold active orders
let totalPurchases = 0; // Variable to hold total purchases
let seasonalBudget = 0; // Variable to hold seasonal budget

function addToCart(cropName, pricePerTon, quantity) {
    const existingItem = cart.find(item => item.name === cropName);
    
    if (existingItem) {
        existingItem.quantity += quantity;
        existingItem.total = existingItem.price * existingItem.quantity; // Update total for the existing item
    } else {
        const item = {
            name: cropName,
            price: pricePerTon,
            quantity: quantity,
            total: pricePerTon * quantity
        };
        cart.push(item); // Add item to cart
    }

    totalAmount = cart.reduce((sum, item) => sum + item.total, 0);
    updateCartDisplay(); // Update the cart display
    updateStats(); // Update stats display
}

function updateCartDisplay() {
    const cartItemsDiv = document.getElementById('cart-items');
    cartItemsDiv.innerHTML = ''; // Clear existing items

    cart.forEach(item => {
        const itemDiv = document.createElement('div');
        itemDiv.className = 'cart-item'; // Add class for styling
        itemDiv.textContent = `${item.name} - Quantity: ${item.quantity}, Price: ₹${item.price.toFixed(2)}, Total: ₹${item.total.toFixed(2)}`;
        cartItemsDiv.appendChild(itemDiv);
    });

    document.getElementById('total-amount').textContent = totalAmount.toFixed(2); // Update total amount display

    // Show confirm purchase button if there are items in the cart
    document.getElementById('confirm-purchase').style.display = cart.length > 0 ? 'block' : 'none';
}

function updateStats() {
    // Update active orders and total purchases
    activeOrders += 1; // Increment active orders
    totalPurchases += 1; // Increment total purchases
    seasonalBudget += totalAmount; // Update seasonal budget

    // Update the display
    document.getElementById('active-orders').textContent = activeOrders;
    document.getElementById('total-purchases').textContent = totalPurchases;
    document.getElementById('seasonal-budget').textContent = seasonalBudget.toFixed(2);
}

// Confirm purchase button functionality
document.getElementById('confirm-purchase').addEventListener('click', () => {
    // Logic to handle the confirmation of the purchase
    alert('Purchase confirmed!'); // Placeholder for confirmation action

    // Reset cart data
    cart = []; // Clear the cart
    totalAmount = 0; // Reset total amount
    updateCartDisplay(); // Update the cart display to reflect the reset
});

// Attach purchaseCrop to the .btn-primary buttons
document.querySelectorAll('.btn-primary').forEach(button => {
    button.addEventListener('click', () => {
        const card = button.closest('.product-card'); // Change to match your HTML structure
        const cropName = card.querySelector('.product-name').textContent; // Get crop name
        const pricePerTon = parseFloat(card.querySelectorAll('.detail-value')[1].textContent.replace('₹', '').replace(',', '').trim()); // Get price per ton (second detail-value)

        const quantity = 1; // You can modify this to get the desired quantity

        addToCart(cropName, pricePerTon, quantity); // Call addToCart
    });
});