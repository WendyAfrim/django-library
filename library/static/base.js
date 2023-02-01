$(document).ready(function () {
    // Toggle the "navbar-burger" class on click
    $(".navbar-burger").click(function () {
        $(".navbar-burger").toggleClass("is-active");
        $(".navbar-menu").toggleClass("is-active");
    });
});

document.addEventListener('DOMContentLoaded', () => {
    (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
        const $notification = $delete.parentNode;

        $delete.addEventListener('click', () => {
            $notification.parentNode.removeChild($notification);
        });
    });
});

// Manage cover image (add/update)
function removeImage() {
    // Reset input file
    $('div.field:has(input[name="cover"])').find('input[type="file"]').val('');
    // Remove image and hide "Remove" button
    $('div.field.has-addons div.control:has(input[name="cover"])').next().hide();
    let img = $('img[name="cover"]');
    if (img != null) {
        img.remove();
    }
}

$('div.field:has(input[name="cover"])').on('change', 'input[type="file"]', function (e) {
    let file = e.target.files[0];
    let reader = new FileReader();
    reader.onload = function (e) {
        // Show "Remove" button
        $('div.field.has-addons div.control:has(input[name="cover"])').next().show();
        // Add image
        $('div.control:has(img[name="cover"]) span.help').remove();
        let img = $('img[name="cover"]');
        img.remove();
        img = document.createElement('img');
        img.width = 100;
        img.name = 'cover';
        $(img).insertBefore('div.field.has-addons:has(input[name="cover"])');
        img.src = e.target.result;
        img.alt = file.name;
    };
    reader.readAsDataURL(file);
});

$(document).ready(function () {
    $('#overdue_only_input').on('change', function () {
        var checked = this.checked;
        $.get({
            url: '/dashboard',
            data: {
                overdue_only: checked
            },
            success: function (data) {
                $('#borrowed-book-table').html($(data).find('#borrowed-book-table').html());
            }
        });
    });
});

$('tr[data-href]').on("click", function() {
    document.location = $(this).data('href');
});