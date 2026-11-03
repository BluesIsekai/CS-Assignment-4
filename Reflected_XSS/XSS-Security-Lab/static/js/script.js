/**
 * XSS SECURITY LAB - Interactive Client Logic
 * Reflected Cross-Site Scripting (XSS) Variant 2
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Mobile Navigation Toggle
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const navLinks = document.getElementById('navLinks');

    if (mobileMenuBtn && navLinks) {
        mobileMenuBtn.addEventListener('click', () => {
            navLinks.classList.toggle('open');
            const isOpen = navLinks.classList.contains('open');
            mobileMenuBtn.innerHTML = isOpen 
                ? '<i class="fa-solid fa-xmark"></i>' 
                : '<i class="fa-solid fa-bars"></i>';
        });
    }

    // 2. Initialize Live Interactive Encoder (Comparison Page)
    initLiveEncoder();
});

/**
 * Sets payload into the search input and automatically submits the form
 * for instant one-click demonstration during practical exams/viva.
 * @param {string} payloadText - The XSS or normal query string
 */
function setPayload(payloadText) {
    const input = document.getElementById('searchQueryInput');
    if (input) {
        // Decode HTML entities if decoded from HTML attribute
        const temp = document.createElement('textarea');
        temp.innerHTML = payloadText;
        const decoded = temp.value;

        input.value = decoded;
        input.focus();

        // Highlight input briefly for visual feedback
        input.style.transition = 'box-shadow 0.2s ease';
        input.style.boxShadow = '0 0 15px rgba(244, 63, 94, 0.7)';
        setTimeout(() => {
            input.style.boxShadow = '';
        }, 600);

        // Auto submit the form
        const form = input.closest('form');
        if (form) {
            form.submit();
        }
    }
}


/**
 * Live Interactive HTML Entity Encoder
 * Updates output dynamically as the student types on the comparison page.
 */
function initLiveEncoder() {
    const liveInput = document.getElementById('liveInput');
    const liveOutput = document.getElementById('liveOutput');
    const detectionBadge = document.getElementById('liveDetectionBadge');
    const detectionText = document.getElementById('detectionText');

    if (!liveInput || !liveOutput) return;

    // Default sample text
    if (!liveInput.value) {
        liveInput.value = "<script>alert('XSS Exploit Proof-of-Concept')</script>";
    }

    const updateEncoding = () => {
        const raw = liveInput.value;
        const dangerousMap = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#x27;'
        };

        let detected = [];
        const encoded = raw.replace(/[&<>"']/g, match => {
            if (!detected.includes(match)) detected.push(match);
            return dangerousMap[match];
        });

        // Update pre tag
        const codeElem = liveOutput.querySelector('code') || liveOutput;
        codeElem.textContent = encoded;

        // Update badge
        if (detectionBadge && detectionText) {
            if (detected.length > 0) {
                detectionBadge.style.color = 'var(--secure-green)';
                detectionText.innerHTML = `Neutralized <strong>${detected.length}</strong> dangerous character type(s): <code>${detected.map(c => escapeHtml(c)).join(' ')}</code>`;
            } else if (raw.trim().length === 0) {
                detectionBadge.style.color = 'var(--text-muted)';
                detectionText.textContent = 'Waiting for input...';
            } else {
                detectionBadge.style.color = 'var(--accent-cyan)';
                detectionText.textContent = 'Safe string: No HTML metacharacters detected.';
            }
        }
    };

    liveInput.addEventListener('input', updateEncoding);
    updateEncoding();
}

/**
 * Helper to escape minimal HTML for badge display
 */
function escapeHtml(str) {
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#x27;');
}
