$(document).ready(function() {
    $(".delete-btn").click(function() {
        var catchId = $(this).closest(".catch-card").data("catch-id");
        // Now you have the catch ID, you can send it to your backend for deletion
        // Example AJAX call to delete the catch with the retrieved ID
        $.ajax({
            url: "/delete-catch",
            method: "POST",
            data: { catchId: catchId },
            success: function(response) {
                // Handle success response
                console.log("Catch deleted successfully");
            },
            error: function(xhr, status, error) {
                // Handle error response
                console.error("Error deleting catch:", error);
            }
        });
    });
});
