function confirmDelete() {
    if (confirm('The Voting Database will be cleared!!!')) {
        document.getElementById("clearDatabaseForm").submit()
    }
}