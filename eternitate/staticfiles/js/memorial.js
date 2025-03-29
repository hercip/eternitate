document.addEventListener('DOMContentLoaded', function() {
    // Initialize timeline animation
    initTimelineAnimation();
    
    // Initialize photo gallery lightbox
    initPhotoGallery();
    
    // Initialize tab navigation
    initTabNavigation();
});

function initTimelineAnimation() {
    const timelineEvents = document.querySelectorAll('.timeline-event');
    if (timelineEvents.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    // Gradually reveal timeline events for aesthetic effect
                    setTimeout(() => {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }, 100);
                }
            });
        }, {
            threshold: 0.1
        });
        
        timelineEvents.forEach(event => {
            event.style.opacity = '0';
            event.style.transform = 'translateY(20px)';
            event.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            observer.observe(event);
        });
    }
}

function initPhotoGallery() {
    const galleryItems = document.querySelectorAll('.gallery-item img');
    
    galleryItems.forEach(item => {
        item.addEventListener('click', function() {
            createLightbox(this.src, this.alt || 'Photo');
        });
    });
}

function createLightbox(src, caption) {
    // Create lightbox container
    const lightbox = document.createElement('div');
    lightbox.classList.add('lightbox');
    
    // Create image element
    const img = document.createElement('img');
    img.src = src;
    img.alt = caption;
    
    // Create caption element if provided
    if (caption && caption !== 'Photo') {
        const captionEl = document.createElement('div');
        captionEl.classList.add('lightbox-caption');
        captionEl.textContent = caption;
        lightbox.appendChild(captionEl);
    }
    
    // Create close button
    const closeBtn = document.createElement('button');
    closeBtn.classList.add('lightbox-close');
    closeBtn.innerHTML = '&times;';
    closeBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        document.body.removeChild(lightbox);
    });
    
    // Add components to lightbox
    lightbox.appendChild(closeBtn);
    lightbox.appendChild(img);
    
    // Add click event to close lightbox
    lightbox.addEventListener('click', function() {
        document.body.removeChild(lightbox);
    });
    
    // Add lightbox to body
    document.body.appendChild(lightbox);
    
    // Add animation
    setTimeout(() => {
        lightbox.classList.add('active');
    }, 10);
    
    // Add key event to close with Escape key
    const handleEscape = function(e) {
        if (e.key === 'Escape' && document.querySelector('.lightbox')) {
            document.body.removeChild(lightbox);
            document.removeEventListener('keydown', handleEscape);
        }
    };
    
    document.addEventListener('keydown', handleEscape);
}

function initTabNavigation() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons and contents
            tabButtons.forEach(btn => btn.classList.remove('active', 'text-blue-500', 'border-b-2', 'border-blue-500'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked button and corresponding content
            const tabId = this.getAttribute('data-tab');
            this.classList.add('active', 'text-blue-500', 'border-b-2', 'border-blue-500');
            document.getElementById(tabId).classList.add('active');
        });
    });
}

// Function to handle form submissions with HTMX
htmx.on('htmx:afterSwap', function(event) {
    if (event.detail.target.id === 'tribute-form-container') {
        document.getElementById('tribute-form').reset();
        initTimelineAnimation();
        initPhotoGallery();
    }
});

// Scroll animation for page sections
function animateOnScroll() {
    const elements = document.querySelectorAll('.animate-on-scroll');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });
    
    elements.forEach(element => {
        observer.observe(element);
    });
}

// Initialize on page load
window.addEventListener('load', function() {
    animateOnScroll();
});
