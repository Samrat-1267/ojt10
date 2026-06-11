document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');

    if (navToggle) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }

    document.addEventListener('click', function(e) {
        if (navMenu && navToggle && !navToggle.contains(e.target) && !navMenu.contains(e.target)) {
            navMenu.classList.remove('active');
        }
    });

    document.querySelectorAll('.message-close').forEach(function(btn) {
        btn.addEventListener('click', function() {
            this.closest('.message').remove();
        });
    });

    setTimeout(function() {
        document.querySelectorAll('.message').forEach(function(msg) {
            msg.style.opacity = '0';
            msg.style.transform = 'translateX(100%)';
            setTimeout(function() {
                msg.remove();
            }, 300);
        });
    }, 5000);

    document.querySelectorAll('.qty-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            const input = this.parentElement.querySelector('.qty-input');
            const min = parseInt(input.getAttribute('min')) || 1;
            const max = parseInt(input.getAttribute('max')) || 999;
            let val = parseInt(input.value) || min;

            if (this.textContent === '+') {
                val = Math.min(val + 1, max);
            } else if (this.textContent === '-') {
                val = Math.max(val - 1, min);
            }
            input.value = val;
        });
    });

    document.querySelectorAll('.add-to-cart').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.dataset.productId;
            const csrfToken = getCsrfToken();

            fetch('/cart/add/' + productId + '/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: 'quantity=1'
            })
            .then(function(response) { return response.json(); })
            .then(function(data) {
                if (data.success) {
                    const badge = document.getElementById('cart-count');
                    if (badge) badge.textContent = data.item_count;
                    showNotification('Added to cart!', 'success');
                }
            })
            .catch(function() {
                showNotification('Error adding to cart', 'error');
            });
        });
    });
});

function getCsrfToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.indexOf(name + '=') === 0) {
            return cookie.substring(name.length + 1);
        }
    }
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.getAttribute('content') : '';
}

function showNotification(message, type) {
    const container = document.querySelector('.messages') || createMessageContainer();
    const msg = document.createElement('div');
    msg.className = 'message message-' + type;
    msg.innerHTML = '<span>' + message + '</span><button class="message-close">&times;</button>';
    container.appendChild(msg);

    msg.querySelector('.message-close').addEventListener('click', function() {
        msg.remove();
    });

    setTimeout(function() {
        msg.style.opacity = '0';
        msg.style.transform = 'translateX(100%)';
        setTimeout(function() {
            msg.remove();
        }, 300);
    }, 4000);
}

function createMessageContainer() {
    const container = document.createElement('div');
    container.className = 'messages';
    document.body.appendChild(container);
    return container;
}
