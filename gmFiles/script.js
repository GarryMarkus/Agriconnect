document.addEventListener('DOMContentLoaded', function() {
    const orders = [
        { id: '001', date: '2023-10-01', status: 'Shipped' },
        { id: '002', date: '2023-10-05', status: 'Processing' },
        { id: '003', date: '2023-10-10', status: 'Delivered' }
    ];

    const orderList = document.getElementById('order-list');
    orders.forEach(order => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${order.id}</td>
            <td>${order.date}</td>
            <td>${order.status}</td>
        `;
        orderList.appendChild(row);
    });
});