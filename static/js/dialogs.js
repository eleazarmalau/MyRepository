// Native dialogs handle keyboard focus, Escape, and focus restoration.
document.addEventListener("click", (event) => {
    const trigger = event.target.closest("[data-delete-dialog]");
    if (trigger) {
        document.getElementById(trigger.dataset.deleteDialog).showModal();
        return;
    }

    const closeButton = event.target.closest("[data-close-dialog]");
    if (closeButton) {
        closeButton.closest("dialog").close();
        return;
    }

    // The content wrapper keeps clicks inside the dialog from dismissing it.
    if (event.target.matches("dialog.delete-dialog")) {
        event.target.close();
    }
});
