/**
 * Main JavaScript for the Event Management System.
 */

const BRL = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' });

/**
 * Formats a raw numeric value as BRL currency and updates the element's text.
 * @param {HTMLElement} el
 * @param {number} value
 */
function setBudgetValue(el, value) {
    el.textContent = BRL.format(value);
}

/**
 * Fetches budget totals from the backend for the selected month/year and
 * updates the three value elements without reloading the page.
 */
function fetchBudgetTotals() {
    const card = document.getElementById('budget-totals-card');
    if (!card) return;

    const url = card.dataset.url;
    const month = document.getElementById('budget-month-filter').value;
    const year = document.getElementById('budget-year-filter').value;

    const approvedEl = document.getElementById('budget-approved-total');
    const sentEl = document.getElementById('budget-sent-total');
    const rejectedEl = document.getElementById('budget-rejected-total');

    // Show loading state
    [approvedEl, sentEl, rejectedEl].forEach(el => {
        el.style.opacity = '0.5';
    });

    fetch(`${url}?month=${month}&year=${year}`, {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
        .then(response => {
            if (!response.ok) throw new Error('Network error');
            return response.json();
        })
        .then(data => {
            setBudgetValue(approvedEl, data.approved);
            setBudgetValue(sentEl, data.sent);
            setBudgetValue(rejectedEl, data.rejected);
        })
        .catch(() => {
            // Silently restore opacity on error; values remain unchanged
        })
        .finally(() => {
            [approvedEl, sentEl, rejectedEl].forEach(el => {
                el.style.opacity = '1';
            });
        });
}

document.addEventListener('DOMContentLoaded', () => {
    // Populate month select dynamically
    const monthFilter = document.getElementById('budget-month-filter');
    if (monthFilter) {
        const months = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho',
                        'Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'];
        const currentMonth = new Date().getMonth() + 1; // 1-12
        months.forEach((name, i) => {
            const opt = new Option(name, i + 1, false, i + 1 === currentMonth);
            monthFilter.appendChild(opt);
        });
        monthFilter.addEventListener('change', fetchBudgetTotals);
    }

    // Format initial values rendered by Django with BRL notation
    document.querySelectorAll('.budget-value[data-raw]').forEach(el => {
        const raw = parseFloat(el.dataset.raw);
        if (!isNaN(raw)) setBudgetValue(el, raw);
    });

    // Wire up year filter dropdown
    const yearFilter = document.getElementById('budget-year-filter');
    if (yearFilter) yearFilter.addEventListener('change', fetchBudgetTotals);
});