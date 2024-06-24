
$(document).ready(function() {

    // events
    htmx.on("messages", function(event) {
        event.detail.value.forEach(createToast);
    });

    $(document).on("click", "[close-msg-btn]", function() {
        $(this).parent().remove();
    });


    const toastTemplate = document.querySelector('[data-toast-template]');
    const toastContainer = document.querySelector('[data-toast-container]');
    function createToast(message) {
        const newToast = toastTemplate.cloneNode(true);
        delete newToast.dataset.toastTemplate;
        newToast.classList.add(message.tags);
        newToast.querySelector('[data-toast-body]').textContent = message.message;
        toastContainer.appendChild(newToast);
        setTimeout(() => toastContainer.contains(newToast) ? htmx.remove(newToast) : null, 4000);
    }

})



