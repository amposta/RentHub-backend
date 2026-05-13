// DOM Ready
document.addEventListener('DOMContentLoaded', function() {
    initNavbar();
    initFloatingAuth();
    initRentalCards();
    initSearch();
});

// Navbar Scroll Effect
function initNavbar() {
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

// Floating Auth Modal
function initFloatingAuth() {
    const floatingBtn = document.getElementById('floatingAuth');
    const authModal = document.getElementById('authModal');
    const closeBtns = document.querySelectorAll('.auth-close');
    
    floatingBtn?.addEventListener('click', () => {
        authModal.classList.add('show');
        document.body.style.overflow = 'hidden';
    });
    
    closeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            authModal.classList.remove('show');
            document.body.style.overflow = 'auto';
        });
    });
    
    // Close on overlay click
    authModal?.addEventListener('click', (e) => {
        if (e.target === authModal) {
            authModal.classList.remove('show');
            document.body.style.overflow = 'auto';
        }
    });
}

// Rental Card Interactions
function initRentalCards() {
    const cards = document.querySelectorAll('.rental-card');
    cards.forEach(card => {
        const heartBtn = card.querySelector('.heart-btn');
        heartBtn?.addEventListener('click', function(e) {
            e.stopPropagation();
            this.classList.toggle('text-red-500');
            this.classList.toggle('fill-current');
        });
    });
}

// Search Functionality (Frontend only)
function initSearch() {
    const searchInput = document.getElementById('searchInput');
    searchInput?.addEventListener('input', function() {
        // Frontend search simulation
        console.log('Searching for:', this.value);
    });
}

// Tab Switching for Auth Modal
function switchTab(tabName) {
    const tabs = document.querySelectorAll('.auth-tab');
    const panels = document.querySelectorAll('.auth-panel-content');
    
    tabs.forEach(tab => tab.classList.remove('bg-orange-500', 'text-white'));
    panels.forEach(panel => panel.classList.add('hidden'));
    
    document.getElementById(`tab-${tabName}`).classList.add('bg-orange-500', 'text-white');
    document.getElementById(`panel-${tabName}`).classList.remove('hidden');
}