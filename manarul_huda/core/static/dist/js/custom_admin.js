document.addEventListener('DOMContentLoaded', function() {
    let lastCount = 0; // Untuk tracking perubahan
    
    // Fungsi untuk update badge
    function updateCommentsBadge(count) {
        const menuItem = document.querySelector('.comments-menu-item');
        if (!menuItem) return;

        // Hanya update jika ada perubahan
        if (count !== lastCount) {
            if (count > 0) {
                menuItem.setAttribute('data-badge', count);
                menuItem.classList.add('has-badge');
            } else {
                menuItem.removeAttribute('data-badge');
                menuItem.classList.remove('has-badge');
            }
            lastCount = count;
        }
    }

    // Fungsi untuk fetch data terbaru
    async function fetchPendingCount() {
        try {
            const response = await fetch('/admin/comments/api/pending-count/');
            if (!response.ok) throw new Error('Network response was not ok');
            const data = await response.json();
            updateCommentsBadge(data.count);
        } catch (error) {
            console.error('Error fetching pending comments count:', error);
        }
    }

    // Fungsi untuk memulai polling
    function startPolling() {
        // Fetch pertama kali
        fetchPendingCount();
        
        // Set interval untuk update selanjutnya
        setInterval(fetchPendingCount, 2000); // Polling setiap 2 detik
    }

    // Initial update dan mulai polling
    const initialCount = document.querySelector('#initial-pending-count');
    if (initialCount) {
        updateCommentsBadge(parseInt(initialCount.value) || 0);
    }
    
    // Mulai polling setelah initial update
    startPolling();
});
