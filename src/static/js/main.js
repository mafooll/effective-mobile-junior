document.addEventListener('DOMContentLoaded', () => {
    try {
        const tooltipTriggerList = Array.from(
            document.querySelectorAll('[data-bs-toggle="tooltip"]')
        );
        tooltipTriggerList.forEach(el => {
            new bootstrap.Tooltip(el);
        });
    } catch (error) {
        console.error('Bootstrap tooltip initialization failed:', error);
    }
});
