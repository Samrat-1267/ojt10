document.addEventListener('DOMContentLoaded', function() {
    function updateCartCount() {
        const xhr = new XMLHttpRequest();
        xhr.open('GET', '/cart/', true);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

        xhr.onload = function() {
            if (xhr.status === 200) {
                try {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(xhr.responseText, 'text/html');
                    const countElements = doc.querySelectorAll('.cart-item');
                    let totalQty = 0;
                    countElements.forEach(function(item) {
                        const qtyInput = item.querySelector('.qty-input');
                        if (qtyInput) {
                            totalQty += parseInt(qtyInput.value) || 0;
                        }
                    });
                    const badge = document.getElementById('cart-count');
                    if (badge) badge.textContent = totalQty;
                } catch(e) {}
            }
        };
        xhr.send();
    }

    document.querySelectorAll('.cart-quantity-form .qty-btn').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            const form = this.closest('.cart-quantity-form');
            const input = form.querySelector('.qty-input');
            const min = parseInt(input.getAttribute('min')) || 1;
            const max = parseInt(input.getAttribute('max')) || 999;
            let val = parseInt(input.value) || min;

            if (this.textContent.includes('+')) {
                val = Math.min(val + 1, max);
            } else {
                val = Math.max(val - 1, min);
            }
            input.value = val;

            const formData = new FormData(form);
            fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken(),
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: formData,
            })
            .then(function(response) {
                if (response.redirected) {
                    window.location.href = response.url;
                }
            });
        });
    });
});
