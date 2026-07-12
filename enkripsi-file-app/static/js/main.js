// This is a placeholder for any future custom JavaScript.
// For now, we can add a simple script to show the filename on the file input.

document.addEventListener('DOMContentLoaded', function () {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(function (input) {
        input.addEventListener('change', function (e) {
            const fileName = e.target.files[0] ? e.target.files[0].name : 'Choose file';
            const nextSibling = e.target.nextElementSibling;
            if (nextSibling && nextSibling.classList.contains('form-label')) {
                nextSibling.innerHTML = fileName;
            }
        });
    });
});