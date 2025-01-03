function handlePaginationClick(event) {
    event.preventDefault(); // Ngăn chặn chuyển hướng mặc định

    // Lấy URL hiện tại
    const currentUrl = new URL(window.location.href);

    // Lấy giá trị của query parameter 'p' từ liên kết được click
    const newPageNumber = event.target.href.split('?p=')[1];

    // Cập nhật query parameter 'p'
    currentUrl.searchParams.set('p', newPageNumber);

    // Chuyển hướng đến URL mới với query parameter 'p' đã được cập nhật
    window.location.href = currentUrl.toString();
}

// Lấy tất cả các liên kết phân trang
const paginationLinks = document.querySelectorAll('.pagination a');

// Gắn sự kiện click cho mỗi liên kết phân trang
paginationLinks.forEach(link => {
    link.addEventListener('click', handlePaginationClick);
});

