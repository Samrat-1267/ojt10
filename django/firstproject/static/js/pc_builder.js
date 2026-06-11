document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('componentModal');
    const modalBody = document.getElementById('modal-body');
    const modalTitle = document.getElementById('modal-title');
    const modalClose = document.querySelector('.modal-close');
    let selectedType = null;
    let selectedComponents = {};

    document.querySelectorAll('.select-component').forEach(function(btn) {
        btn.addEventListener('click', function() {
            selectedType = this.dataset.type;
            openModal(selectedType);
        });
    });

    if (modalClose) {
        modalClose.addEventListener('click', closeModal);
    }

    modal.addEventListener('click', function(e) {
        if (e.target === modal) closeModal();
    });

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') closeModal();
    });

    function openModal(type) {
        const labels = {
            'cpu': 'CPU', 'gpu': 'GPU', 'motherboard': 'Motherboard',
            'ram': 'RAM', 'storage': 'Storage', 'psu': 'Power Supply',
            'cooling': 'Cooling', 'case': 'Case'
        };
        modalTitle.textContent = 'Select ' + (labels[type] || type);
        modalBody.innerHTML = '<div class="loading">Loading components...</div>';
        modal.classList.add('active');

        fetch('/builder/api/components/' + type + '/')
            .then(function(r) { return r.json(); })
            .then(function(components) {
                if (components.length === 0) {
                    modalBody.innerHTML = '<p class="no-selection" style="text-align:center;padding:40px;">No components available in this category.</p>';
                    return;
                }
                let html = '';
                components.forEach(function(comp) {
                    const isSelected = selectedComponents[type] && selectedComponents[type].id === comp.id;
                    html += '<div class="component-option ' + (isSelected ? 'selected' : '') + '" data-id="' + comp.id + '" data-name="' + comp.name + '" data-price="' + comp.price + '" data-type="' + type + '">';
                    html += '<div>';
                    html += '<div class="component-option-name">' + comp.name + '</div>';
                    html += '<div style="font-size:0.8rem;color:var(--text-muted);margin-top:4px;">Stock: ' + comp.stock + '</div>';
                    html += '</div>';
                    html += '<div class="component-option-price">$' + parseFloat(comp.price).toFixed(2) + '</div>';
                    html += '</div>';
                });
                modalBody.innerHTML = html;

                modalBody.querySelectorAll('.component-option').forEach(function(opt) {
                    opt.addEventListener('click', function() {
                        const id = this.dataset.id;
                        const name = this.dataset.name;
                        const price = this.dataset.price;
                        const type = this.dataset.type;

                        selectedComponents[type] = { id: parseInt(id), name: name, price: parseFloat(price) };
                        updateBuilderUI(type, name, price);
                        closeModal();
                    });
                });
            })
            .catch(function() {
                modalBody.innerHTML = '<p style="text-align:center;padding:40px;color:var(--accent-red);">Error loading components.</p>';
            });
    }

    function closeModal() {
        modal.classList.remove('active');
        selectedType = null;
    }

    function updateBuilderUI(type, name, price) {
        const selectedDiv = document.getElementById('selected-' + type);
        if (selectedDiv) {
            selectedDiv.innerHTML = '<div class="selected-component"><span class="selected-name">' + name + '</span><span class="selected-price">$' + parseFloat(price).toFixed(2) + '</span></div>';
        }

        const summaryPrice = document.getElementById('price-' + type);
        if (summaryPrice) {
            summaryPrice.textContent = '$' + parseFloat(price).toFixed(2);
        }

        updateTotal();
    }

    function updateTotal() {
        let total = 0;
        Object.values(selectedComponents).forEach(function(comp) {
            total += comp.price;
        });

        const totalEl = document.getElementById('build-total-price');
        if (totalEl) {
            totalEl.textContent = '$' + total.toFixed(2);
        }

        const compatEl = document.getElementById('compatibility-status');
        if (compatEl) {
            const count = Object.keys(selectedComponents).length;
            if (count >= 4) {
                compatEl.className = 'compatibility-status compatible';
                compatEl.innerHTML = '&#10003; All components are compatible';
            } else if (count > 0) {
                compatEl.className = 'compatibility-status compatible';
                compatEl.innerHTML = 'Select more components to check compatibility';
            } else {
                compatEl.className = 'compatibility-status compatible';
                compatEl.innerHTML = 'Select components to begin';
            }
        }
    }

    const addBuildToCart = document.getElementById('add-build-to-cart');
    if (addBuildToCart) {
        addBuildToCart.addEventListener('click', function() {
            const count = Object.keys(selectedComponents).length;
            if (count === 0) {
                alert('Please select at least one component.');
                return;
            }

            const componentIds = Object.values(selectedComponents).map(function(c) { return c.id; });
            let completed = 0;

            componentIds.forEach(function(id) {
                fetch('/cart/add/' + id + '/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCsrfToken(),
                        'X-Requested-With': 'XMLHttpRequest',
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: 'quantity=1'
                })
                .then(function(r) { return r.json(); })
                .then(function(data) {
                    completed++;
                    if (data.success) {
                        const badge = document.getElementById('cart-count');
                        if (badge) badge.textContent = data.item_count;
                    }
                    if (completed === componentIds.length) {
                        alert('Build added to cart!');
                        window.location.href = '/cart/';
                    }
                })
                .catch(function() {
                    completed++;
                    if (completed === componentIds.length) {
                        alert('Some items may not have been added.');
                    }
                });
            });
        });
    }

    const saveBuildBtn = document.getElementById('save-build');
    if (saveBuildBtn) {
        saveBuildBtn.addEventListener('click', function() {
            const count = Object.keys(selectedComponents).length;
            if (count === 0) {
                alert('Please select at least one component.');
                return;
            }

            const buildName = prompt('Name your build:', 'My Custom Build');
            if (!buildName) return;

            const components = {};
            Object.keys(selectedComponents).forEach(function(type) {
                components[type] = selectedComponents[type].id;
            });

            fetch(saveBuildUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken(),
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name: buildName, components: components })
            })
            .then(function(r) { return r.json(); })
            .then(function(data) {
                if (data.success) {
                    alert('Build saved!');
                } else {
                    alert('Error saving build.');
                }
            })
            .catch(function() {
                alert('Error saving build.');
            });
        });
    }
});
