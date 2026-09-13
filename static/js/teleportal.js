// TELEPORTAL Client JavaScript Utilities
(function() {
  // Apply saved theme immediately
  const savedTheme = localStorage.getItem("teleportal_theme");
  if (savedTheme === "dark") {
    document.documentElement.setAttribute("data-bs-theme", "dark");
    if (document.body) document.body.classList.add("dark-mode");
  }
})();

document.addEventListener("DOMContentLoaded", function() {
  // Dark Mode Toggle
  const themeToggle = document.getElementById("themeToggle");
  const isCurrentlyDark = localStorage.getItem("teleportal_theme") === "dark";
  
  if (isCurrentlyDark) {
    document.documentElement.setAttribute("data-bs-theme", "dark");
    document.body.classList.add("dark-mode");
    if (themeToggle) {
      themeToggle.innerHTML = '<i class="bi bi-sun-fill text-warning"></i>';
    }
  }

  if (themeToggle) {
    themeToggle.addEventListener("click", function() {
      const isDark = document.body.classList.toggle("dark-mode");
      document.documentElement.setAttribute("data-bs-theme", isDark ? "dark" : "light");
      localStorage.setItem("teleportal_theme", isDark ? "dark" : "light");
      themeToggle.innerHTML = isDark ? '<i class="bi bi-sun-fill text-warning"></i>' : '<i class="bi bi-moon-stars-fill"></i>';
    });
  }

  // Load Unread Notifications
  const notifCount = document.getElementById("notifCount");
  const notifList = document.getElementById("notifList");
  if (notifCount && notifList) {
    fetch("/api/notifications/unread")
      .then(res => res.json())
      .then(data => {
        if (data.count > 0) {
          notifCount.innerText = data.count;
          notifCount.classList.remove("d-none");
          notifList.innerHTML = data.notifications.map(n => `
            <li>
              <a class="dropdown-item py-2" href="${n.link}">
                <strong>${n.title}</strong>
                <div class="small text-muted">${n.message}</div>
                <div class="smaller text-secondary">${n.time}</div>
              </a>
            </li>
          `).join("");
        } else {
          notifList.innerHTML = '<li><span class="dropdown-item text-muted">No new notifications</span></li>';
        }
      })
      .catch(() => {});
  }
});