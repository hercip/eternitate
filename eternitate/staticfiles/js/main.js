// General animations and interactive elements

document.addEventListener('DOMContentLoaded', function() {
    // Add fade-in animation to the main content
    const mainContent = document.querySelector('main');
    if (mainContent) {
        mainContent.classList.add('fade-in');
    }
    
    // Add smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 100,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Initialize any tooltips
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(tooltip => {
        tooltip.addEventListener('mouseenter', function() {
            const tooltipText = this.getAttribute('data-tooltip');
            
            const tooltipElement = document.createElement('div');
            tooltipElement.classList.add('tooltip');
            tooltipElement.textContent = tooltipText;
            
            document.body.appendChild(tooltipElement);
            
            const rect = this.getBoundingClientRect();
            tooltipElement.style.top = rect.bottom + 10 + 'px';
            tooltipElement.style.left = rect.left + rect.width / 2 - tooltipElement.offsetWidth / 2 + 'px';
            
            tooltipElement.classList.add('visible');
        });
        
        tooltip.addEventListener('mouseleave', function() {
            const tooltipElement = document.querySelector('.tooltip');
            if (tooltipElement) {
                tooltipElement.remove();
            }
        });
    });
    
    // Add input animations for form fields
    const formInputs = document.querySelectorAll('input, textarea');
    formInputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('input-focused');
        });
        
        input.addEventListener('blur', function() {
            if (!this.value) {
                this.parentElement.classList.remove('input-focused');
            }
        });
        
        // Initialize state for inputs with values
        if (input.value) {
            input.parentElement.classList.add('input-focused');
        }
    });
});

// Memorial page specific functionality
function initMemorialPage() {
    // Add lightbox functionality for photos
    const galleryItems = document.querySelectorAll('.gallery-item img');
    if (galleryItems.length > 0) {
        galleryItems.forEach(item => {
            item.addEventListener('click', function() {
                const lightbox = document.createElement('div');
                lightbox.classList.add('lightbox');
                
                const imgElement = document.createElement('img');
                imgElement.src = this.src;
                
                lightbox.appendChild(imgElement);
                document.body.appendChild(lightbox);
                
                lightbox.addEventListener('click', function() {
                    this.remove();
                });
            });
        });
    }
    
    // Add timeline animations
    const timelineEvents = document.querySelectorAll('.timeline-event');
    if (timelineEvents.length > 0) {
        // Add scroll animation for timeline events
        const animateOnScroll = function() {
            timelineEvents.forEach(event => {
                const eventPosition = event.getBoundingClientRect();
                const windowHeight = window.innerHeight;
                
                if (eventPosition.top < windowHeight * 0.8) {
                    event.classList.add('visible');
                }
            });
        };
        
        // Run once on load
        animateOnScroll();
        
        // Listen for scroll events
        window.addEventListener('scroll', animateOnScroll);
    }
}

// Initialize memorial page if we're on one
if (document.querySelector('.memorial-page')) {
    initMemorialPage();
}
