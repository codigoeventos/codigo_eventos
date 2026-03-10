/**
 * Main JavaScript for the Event Management System.
 */

const BRL = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' });

/**
 * Formats a raw numeric value as BRL currency and updates the element's text.
 * @param {HTMLElement} el
 * @param {number} value
 */
function setProposalValue(el, value) {
    el.textContent = BRL.format(value);
}

/**
 * Fetches proposal totals from the backend for the selected month/year and
 * updates the three value elements without reloading the page.
 */
function fetchProposalTotals() {
    const card = document.getElementById('proposal-totals-card');
    if (!card) return;

    const url = card.dataset.url;
    const month = document.getElementById('proposal-month-filter').value;
    const year = document.getElementById('proposal-year-filter').value;

    const approvedEl = document.getElementById('proposal-approved-total');
    const sentEl = document.getElementById('proposal-sent-total');
    const rejectedEl = document.getElementById('proposal-rejected-total');

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
            setProposalValue(approvedEl, data.approved);
            setProposalValue(sentEl, data.sent);
            setProposalValue(rejectedEl, data.rejected);
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
    const monthFilter = document.getElementById('proposal-month-filter');
    if (monthFilter) {
        const months = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho',
                        'Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'];
        const currentMonth = new Date().getMonth() + 1; // 1-12
        months.forEach((name, i) => {
            const opt = new Option(name, i + 1, false, i + 1 === currentMonth);
            monthFilter.appendChild(opt);
        });
        monthFilter.addEventListener('change', fetchProposalTotals);
    }

    // Format initial values rendered by Django with BRL notation
    document.querySelectorAll('.proposal-value[data-raw]').forEach(el => {
        const raw = parseFloat(el.dataset.raw);
        if (!isNaN(raw)) setProposalValue(el, raw);
    });

    // Wire up year filter dropdown
    const yearFilter = document.getElementById('proposal-year-filter');
    if (yearFilter) yearFilter.addEventListener('change', fetchProposalTotals);
});