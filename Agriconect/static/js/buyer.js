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
    document.querySelectorAll('.btn-primary').forEach(button => {
        button.addEventListener('click', function() {
            const productCard = this.closest('.product-card');
            const productName = productCard.querySelector('.product-name').textContent;
            const priceText = productCard.querySelector('.detail-value').textContent;
            const price = parseFloat(priceText.replace(/[^0-9.]/g, ''));
            addToCart(productName, price, 1);
        });
    });

    loadOrderHistory();

    // Calculate total amount from all product cards
    function calculateTotalAmount() {
        const productCards = document.querySelectorAll('.product-card');
        let total = 0;
        
        productCards.forEach(card => {
            const priceText = card.querySelector('.detail-value').textContent;
            const price = parseFloat(priceText.replace(/[^0-9.]/g, ''));
            if (!isNaN(price)) {
                total += price;
            }
        });
        
        // Update the seasonal budget display
        const seasonalBudgetElement = document.getElementById('seasonal-budget');
        if (seasonalBudgetElement) {
            seasonalBudgetElement.textContent = formatCurrency(total);
        }
        
        return total;
    }

    // Calculate initial total
    calculateTotalAmount();

    const confirmButton = document.getElementById('confirm-purchase');
    if (confirmButton) {
        confirmButton.addEventListener('click', confirmPurchase);
    }
});

document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('click', function() {
        const action = this.textContent;
        const productCard = this.closest('.product-card');
        const productName = productCard.querySelector('.product-name').textContent;
        console.log(`${action} clicked for ${productName}`);
    });
});

let cart = []; 
let totalAmount = 0; 
let activeOrders = 0; 
let totalPurchases = 0; 
let seasonalBudget = 0; 

function addToCart(cropName, pricePerTon, quantity) {
    const existingItem = cart.find(item => item.name === cropName);
    
    if (existingItem) {
        existingItem.quantity += quantity;
        existingItem.total = existingItem.price * existingItem.quantity;
    } else {
        const item = {
            name: cropName,
            price: pricePerTon,
            quantity: quantity,
            total: pricePerTon * quantity
        };
        cart.push(item);
    }

    totalAmount = cart.reduce((sum, item) => sum + item.total, 0);
    updateCartDisplay();
    
    const confirmButton = document.getElementById('confirm-purchase');
    if (confirmButton) {
        confirmButton.style.display = cart.length > 0 ? 'block' : 'none';
    }
}

function updateCartDisplay() {
    const cartItemsDiv = document.getElementById('cart-items');
    cartItemsDiv.innerHTML = ''; 
    cart.forEach(item => {
        const itemDiv = document.createElement('div');
        itemDiv.className = 'cart-item';
        itemDiv.textContent = `${item.name} - Quantity: ${item.quantity}, Price: ${formatCurrency(item.price)}, Total: ${formatCurrency(item.total)}`;
        cartItemsDiv.appendChild(itemDiv);
    });


    const totalAmountSpan = document.getElementById('total-amount');
    if (totalAmountSpan) {
        totalAmountSpan.textContent = formatCurrency(totalAmount);
    }

    document.getElementById('confirm-purchase').style.display = cart.length > 0 ? 'block' : 'none';
}

function updateStats() {
    
    activeOrders += 1; 
    totalPurchases += 1; 
    seasonalBudget += totalAmount; 

    
    document.getElementById('active-orders').textContent = activeOrders;
    document.getElementById('total-purchases').textContent = totalPurchases;
    document.getElementById('seasonal-budget').textContent = formatCurrency(seasonalBudget);
}


function updateDashboardStats(data) {
    document.getElementById('active-orders').textContent = data.active_orders_count;
    document.getElementById('total-purchases').textContent = data.total_purchases;
    document.getElementById('seasonal-budget').textContent = formatCurrency(data.total_spent);
}


function formatCurrency(amount) {
    return `₹ ${parseFloat(amount).toLocaleString('en-IN', {
        maximumFractionDigits: 2,
        minimumFractionDigits: 2
    })}`;
}


function getStatusBadgeClass(status) {
    const statusClasses = {
        'pending': 'badge-warning',
        'confirmed': 'badge-info',
        'processing': 'badge-primary',
        'completed': 'badge-success',
        'cancelled': 'badge-danger'
    };
    return statusClasses[status] || 'badge-secondary';
}

async function confirmPurchase() {
    try {
        const response = await fetch('/create_order/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                cart: cart,
                totalAmount: totalAmount
            })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            // Clear the cart
            cart = [];
            totalAmount = 0;
            updateCartDisplay();
            
         
            loadOrderHistory();
            
            alert('Order created successfully!');
        } else {
            alert('Error: ' + data.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error creating order. Please try again.');
    }
}


async function loadOrderHistory() {
    try {
        const response = await fetch('/get_order_history/');
        const data = await response.json();
        
        if (data.status === 'success') {
        
            updateDashboardStats(data);
            
            const historyContainer = document.getElementById('cart-items');
            historyContainer.innerHTML = '<h3>Order History</h3>';
            
            if (data.orders.length === 0) {
                historyContainer.innerHTML += '<p class="no-orders">No orders found</p>';
                return;
            }
            
          
            const ordersContainer = document.createElement('div');
            ordersContainer.className = 'orders-container';
            
            data.orders.forEach(order => {
                const orderDiv = document.createElement('div');
                orderDiv.className = 'order-item';
                
                let itemsHtml = '';
                order.items.forEach(item => {
                    itemsHtml += `
                        <div class="order-item-detail">
                            ${item.name} - Quantity: ${item.quantity}, Price: ${formatCurrency(item.price)}
                        </div>
                    `;
                });
                
                orderDiv.innerHTML = `
                    <div class="order-header">
                        <span>Order #${order.order_number}</span>
                        <span>Date: ${order.created_at}</span>
                        <span class="status-badge ${getStatusBadgeClass(order.status)}">${order.status.toUpperCase()}</span>
                    </div>
                    <div class="order-items">
                        ${itemsHtml}
                    </div>
                    <div class="order-total">
                        Total Amount: ${formatCurrency(order.total_amount)}
                    </div>
                `;
                ordersContainer.appendChild(orderDiv);
            });
            
            historyContainer.appendChild(ordersContainer);
            
         
            const totalAmountSpan = document.getElementById('total-amount');
            if (totalAmountSpan) {
                totalAmountSpan.textContent = formatCurrency(data.total_spent);
            }
        }
    } catch (error) {
        console.error('Error:', error);
    }
}