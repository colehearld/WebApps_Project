$(document).ready(function() {
    $(".delete-btn").click(function() {
        var catchId = $(this).closest(".catch-card").data("catch-id");
        $.ajax({
            url: "/delete-catch",
            method: "POST",
            data: { catchId: catchId },
            success: function(response) {
                console.log("Catch deleted successfully");
            },
            error: function(xhr, status, error) {
                console.error("Error deleting catch:", error);
            }
        });
    });
});
