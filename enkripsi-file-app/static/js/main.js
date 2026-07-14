/**
 * SecureCrypt - Main JavaScript
 * Interactivity & UI Enhancements
 */

document.addEventListener('DOMContentLoaded', function() {
    'use strict';

    // ============================================
    // 1. FLASH MESSAGES AUTO-DISMISS
    // ============================================
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(function(msg) {
        // Auto dismiss after 5 seconds
        setTimeout(function() {
            msg.style.transition = 'all 0.3s ease';
            msg.style.opacity = '0';
            msg.style.transform = 'translateY(-10px)';
            setTimeout(function() {
                msg.remove();
            }, 300);
        }, 5000);
        
        // Close button
        const closeBtn = msg.querySelector('.flash-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                msg.remove();
            });
        }
    });

    // ============================================
    // 2. NAVBAR TOGGLE (Mobile)
    // ============================================
    const navToggler = document.querySelector('.navbar-toggler');
    const navCollapse = document.querySelector('#main-nav');
    
    if (navToggler && navCollapse) {
        navToggler.addEventListener('click', function() {
            const expanded = this.getAttribute('aria-expanded') === 'true' ? false : true;
            this.setAttribute('aria-expanded', expanded);
        });
    }

    // ============================================
    // 3. DROP ZONE (Encrypt & Decrypt)
    // ============================================
    const dropZones = document.querySelectorAll('.drop-zone');
    
    dropZones.forEach(function(zone) {
        const fileInput = zone.parentElement.querySelector('input[type="file"]');
        if (!fileInput) return;
        
        // Click to open file dialog
        zone.addEventListener('click', function(e) {
            // Prevent if clicking remove button
            if (e.target.closest('.remove-file')) return;
            fileInput.click();
        });
        
        // Drag over
        zone.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.classList.add('dragover');
        });
        
        // Drag leave
        zone.addEventListener('dragleave', function(e) {
            e.preventDefault();
            this.classList.remove('dragover');
        });
        
        // Drop
        zone.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                fileInput.dispatchEvent(new Event('change'));
            }
        });
        
        // File input change
        fileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                updateFilePreview(this.closest('.drop-zone'), this.files[0]);
            }
        });
        
        // Remove file button
        const removeBtn = zone.querySelector('.remove-file');
        if (removeBtn) {
            removeBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                const zone = this.closest('.drop-zone');
                const input = zone.querySelector('input[type="file"]');
                if (input) {
                    input.value = '';
                    input.dispatchEvent(new Event('change'));
                }
                resetDropZone(zone);
            });
        }
    });
    
    function updateFilePreview(zone, file) {
        const content = zone.querySelector('.drop-zone-content');
        const preview = zone.querySelector('.file-preview');
        const fileName = zone.querySelector('.file-name');
        const fileSize = zone.querySelector('.file-size');
        const fileMethod = zone.querySelector('.file-method');
        
        if (content) content.style.display = 'none';
        if (preview) preview.style.display = 'block';
        
        if (fileName) fileName.textContent = file.name;
        if (fileSize) {
            const size = (file.size / 1024 / 1024).toFixed(2);
            fileSize.textContent = size + ' MB';
        }
        
        // Detect method from extension (for decrypt page)
        if (fileMethod) {
            if (file.name.endsWith('.aes')) {
                fileMethod.textContent = '🔐 AES-256';
                selectMethod('aes');
            } else if (file.name.endsWith('.fernet')) {
                fileMethod.textContent = '🔑 Fernet';
                selectMethod('fernet');
            } else {
                fileMethod.textContent = '📄 Unknown';
            }
        }
    }
    
    function resetDropZone(zone) {
        const content = zone.querySelector('.drop-zone-content');
        const preview = zone.querySelector('.file-preview');
        const progress = zone.querySelector('.progress-bar');
        
        if (content) content.style.display = 'block';
        if (preview) preview.style.display = 'none';
        if (progress) progress.style.width = '0%';
    }
    
    function selectMethod(method) {
        const cards = document.querySelectorAll('.method-card');
        cards.forEach(function(card) {
            const radio = card.querySelector('input[type="radio"]');
            if (radio && radio.value === method) {
                card.classList.add('active');
                radio.checked = true;
            } else {
                card.classList.remove('active');
            }
        });
    }

    // ============================================
    // 4. METHOD SELECTOR
    // ============================================
    const methodCards = document.querySelectorAll('.method-card');
    methodCards.forEach(function(card) {
        card.addEventListener('click', function() {
            const parent = this.closest('.method-grid');
            if (parent) {
                parent.querySelectorAll('.method-card').forEach(function(c) {
                    c.classList.remove('active');
                });
            }
            this.classList.add('active');
            const radio = this.querySelector('input[type="radio"]');
            if (radio) {
                radio.checked = true;
            }
        });
    });

    // ============================================
    // 5. PASSWORD TOGGLE
    // ============================================
    const toggleButtons = document.querySelectorAll('.toggle-password');
    toggleButtons.forEach(function(btn) {
        btn.addEventListener('click', function() {
            const input = this.parentElement.querySelector('input[type="password"], input[type="text"]');
            if (!input) return;
            
            const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
            input.setAttribute('type', type);
            
            const icon = this.querySelector('i');
            if (icon) {
                icon.classList.toggle('bi-eye');
                icon.classList.toggle('bi-eye-slash');
            }
        });
    });

    // ============================================
    // 6. PASSWORD STRENGTH (Encrypt Page)
    // ============================================
    const passwordInputs = document.querySelectorAll('#password');
    passwordInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            const strength = calculateStrength(this.value);
            const wrapper = this.closest('.password-wrapper');
            if (!wrapper) return;
            
            const container = wrapper.parentElement;
            const bar = container.querySelector('.strength-bar');
            const text = container.querySelector('.strength-text');
            
            if (!bar || !text) return;
            
            const levels = ['', 'Lemah', 'Sedang', 'Kuat', 'Sangat Kuat'];
            const colors = ['', '#EF4444', '#F59E0B', '#10B981', '#34D399'];
            
            bar.style.width = (strength * 25) + '%';
            bar.style.background = colors[strength];
            text.textContent = levels[strength] || 'Kekuatan password';
        });
    });
    
    function calculateStrength(password) {
        let score = 0;
        if (password.length >= 6) score++;
        if (password.length >= 10) score++;
        if (/[A-Z]/.test(password)) score++;
        if (/[0-9]/.test(password)) score++;
        if (/[^A-Za-z0-9]/.test(password)) score++;
        return Math.min(score, 4);
    }

    // ============================================
    // 7. FORM SUBMIT LOADING STATE
    // ============================================
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            // Check if there's a file input
            const fileInput = this.querySelector('input[type="file"]');
            if (fileInput) {
                const zone = this.querySelector('.drop-zone');
                if (zone && (!fileInput.files || fileInput.files.length === 0)) {
                    e.preventDefault();
                    zone.style.borderColor = '#f87171';
                    zone.style.background = 'rgba(248, 113, 113, 0.08)';
                    setTimeout(function() {
                        zone.style.borderColor = '';
                        zone.style.background = '';
                    }, 2000);
                    return;
                }
            }
            
            // Show loading on submit button
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                const icon = submitBtn.querySelector('i');
                const loader = submitBtn.querySelector('.btn-loader');
                
                if (loader) {
                    submitBtn.disabled = true;
                    if (icon) icon.classList.add('d-none');
                    loader.classList.remove('d-none');
                }
            }
        });
    });

    // ============================================
    // 8. ANIMATED STATS COUNTER (Home Page)
    // ============================================
    const statNumbers = document.querySelectorAll('.stat-number');
    statNumbers.forEach(function(counter) {
        const target = parseFloat(counter.getAttribute('data-count'));
        if (isNaN(target)) return;
        
        const duration = 2000;
        const step = target / (duration / 16);
        let current = 0;
        let animated = false;
        
        function updateCounter() {
            if (animated) return;
            current += step;
            if (current < target) {
                counter.textContent = Math.round(current);
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target;
                animated = true;
            }
        }
        
        const observer = new IntersectionObserver(function(entries) {
            if (entries[0].isIntersecting && !animated) {
                updateCounter();
                observer.unobserve(counter);
            }
        }, { threshold: 0.5 });
        
        observer.observe(counter);
    });

    // ============================================
    // 9. TOOLTIP INITIALIZATION (Bootstrap)
    // ============================================
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    if (tooltips.length > 0 && typeof bootstrap !== 'undefined') {
        tooltips.forEach(function(el) {
            new bootstrap.Tooltip(el);
        });
    }

    // ============================================
    // 10. KEYBOARD SHORTCUTS
    // ============================================
    document.addEventListener('keydown', function(e) {
        // Ctrl+E = Go to encrypt
        if (e.ctrlKey && e.key === 'e') {
            e.preventDefault();
            const encryptLink = document.querySelector('a[href*="encrypt"]');
            if (encryptLink) encryptLink.click();
        }
        // Ctrl+D = Go to decrypt
        if (e.ctrlKey && e.key === 'd') {
            e.preventDefault();
            const decryptLink = document.querySelector('a[href*="decrypt"]');
            if (decryptLink) decryptLink.click();
        }
    });

    // ============================================
    // 11. CONSOLE WELCOME
    // ============================================
    console.log('%c🔐 SecureCrypt', 'font-size: 24px; font-weight: 700; color: #38bdf8;');
    console.log('%cKeamanan data adalah prioritas utama', 'font-size: 14px; color: #93a1b7;');
    console.log('%c💡 Tips: Ctrl+E untuk enkripsi, Ctrl+D untuk dekripsi', 'font-size: 12px; color: #5b6b85;');
});