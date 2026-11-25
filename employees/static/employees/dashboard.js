// Employee Records page: show/hide the list and keep the status message up to date.
(function () {
  "use strict";

  const list = document.getElementById("employee-list");
  const toggleBtn = document.getElementById("toggle-list");
  const statusMsg = document.getElementById("dashboard-status");
  const emptyState = document.getElementById("empty-state");
  if (!list || !toggleBtn || !statusMsg) return; // not this page

  const plural = (n) => (n === 1 ? "employee" : "employees");

  function updateStatus() {
    const total = list.querySelectorAll(".emp-card").length;
    const active = list.querySelectorAll('.emp-card[data-active="true"]').length;
    if (emptyState) emptyState.hidden = total > 0;
    if (list.hidden) {
      statusMsg.textContent = "Employee list is hidden (" + total + " " + plural(total) + " in total).";
    } else if (total === 0) {
      statusMsg.textContent = "There are no employees to show.";
    } else {
      statusMsg.textContent = "Showing " + total + " " + plural(total) + " (" + active + " active).";
    }
  }

  toggleBtn.addEventListener("click", function () {
    const willShow = list.hidden;
    list.hidden = !willShow;
    toggleBtn.textContent = willShow ? "Hide Employees" : "Show Employees";
    toggleBtn.setAttribute("aria-expanded", String(willShow));
    updateStatus();
  });

  updateStatus();
})();