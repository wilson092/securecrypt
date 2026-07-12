document.addEventListener('DOMContentLoaded', function () {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file');
    const fileInfo = document.getElementById('file-info');
    const form = document.querySelector('form');
    const submitBtn = form ? form.querySelector('button[type="submit"]') : null;

    if (dropZone && fileInput && fileInfo) {
        // --- Drag and Drop Logic ---
        dropZone.addEventListener('click', () => fileInput.click());

        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('drag-over');
        });

        dropZone.addEventListener('dragleave', (e) => {
            e.preventDefault();
            dropZone.classList.remove('drag-over');
        });

        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('drag-over');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                updateFileInfo(files[0]);
            }
        });

        fileInput.addEventListener('change', () => {
            const files = fileInput.files;
            if (files.length > 0) {
                updateFileInfo(files[0]);
            }
        });

        function updateFileInfo(file) {
            const sizeInMB = (file.size / (1024 * 1024)).toFixed(2);
            fileInfo.innerHTML = `
                <i class="bi bi-file-earmark-arrow-up-fill fs-1 text-success"></i>
                <div class="mt-2">
                    <strong>${file.name}</strong> (${sizeInMB} MB)
                </div>
            `;
        }
    }

    // --- Form Submission Loading State ---
    if (form && submitBtn) {
        form.addEventListener('submit', function () {
            // Basic validation
            if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
                // If there's no file input on the page, or no file selected, don't show spinner.
                // This might be handled by `required` attribute, but it's a good fallback.
                return;
            }

            const originalText = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = `
                <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                Processing...
            `;

            // Optional: revert button state if user navigates back without page reload
            window.addEventListener('pageshow', function(event) {
                if (event.persisted) {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }
            });
        });
    }
});