// Employee Dashboard: client-side behaviour only (nothing here is saved to the server).
(function () {
  "use strict";

  // 1. Select the DOM elements we need
  const list = document.getElementById("employee-list");
  const toggleBtn = document.getElementById("toggle-list");
  const statusMsg = document.getElementById("dashboard-status");
  const emptyState = document.getElementById("empty-state");
  const form = document.getElementById("employee-form");
  const messages = document.getElementById("form-messages");
  if (!list || !toggleBtn || !form) return; // not the dashboard page

  const fields = {
    name: { input: document.getElementById("emp-name"), error: document.getElementById("emp-name-error") },
    email: { input: document.getElementById("emp-email"), error: document.getElementById("emp-email-error") },
    department: { input: document.getElementById("emp-department"), error: document.getElementById("emp-department-error") },
    title: { input: document.getElementById("emp-title"), error: document.getElementById("emp-title-error") },
  };

  const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const validators = {
    name: (v) => (v ? "" : "Please enter the employee name."),
    email: (v) => (!v ? "Please enter the email address." : EMAIL_PATTERN.test(v) ? "" : "Please enter a valid email address."),
    department: (v) => (v ? "" : "Please select a department."),
    title: (v) => (v ? "" : "Please enter the job title."),
  };

  // 2. Helpers
  const plural = (n) => (n === 1 ? "employee" : "employees");

  function el(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function updateStatus() {
    const total = list.querySelectorAll(".emp-card").length;
    const active = list.querySelectorAll('.emp-card[data-active="true"]').length;
    emptyState.hidden = total > 0;
    if (list.hidden) {
      statusMsg.textContent = "Employee list is hidden (" + total + " " + plural(total) + " in total).";
    } else if (total === 0) {
      statusMsg.textContent = "There are no employees to show.";
    } else {
      statusMsg.textContent = "Showing " + total + " " + plural(total) + " (" + active + " active).";
    }
  }

  function showMessage(type, text) {
    messages.textContent = text;
    messages.className = "form-msg " + type;
    messages.hidden = false;
  }

  function clearMessage() {
    messages.textContent = "";
    messages.className = "form-msg";
    messages.hidden = true;
  }

  function validateField(key) {
    const field = fields[key];
    const message = validators[key](field.input.value.trim());
    field.error.textContent = message;
    field.input.setAttribute("aria-invalid", message ? "true" : "false");
    field.input.classList.toggle("invalid", Boolean(message));
    return message;
  }

  function hasInvalidField() {
    return Object.keys(fields).some((key) => fields[key].input.getAttribute("aria-invalid") === "true");
  }

  function clearFieldErrors() {
    Object.keys(fields).forEach((key) => {
      fields[key].error.textContent = "";
      fields[key].input.removeAttribute("aria-invalid");
      fields[key].input.classList.remove("invalid");
    });
  }

  // 3. Build a new employee card with createElement()
  function actionButton(action, label) {
    const button = el("button", "btn ghost small", label);
    button.type = "button";
    button.dataset.action = action;
    return button;
  }

  function createEmployeeCard(employee) {
    const card = el("article", "emp-card");
    card.dataset.active = "true";

    const info = el("div");
    info.append(
      el("h3", "", employee.name),
      el("p", "", employee.title + " · " + employee.department),
      el("p", "muted", employee.email)
    );
    const top = el("div", "emp-top");
    top.append(info, el("span", "pill active", "Active"));

    const actions = el("div", "emp-actions");
    actions.append(actionButton("toggle-status", "Mark inactive"), actionButton("remove", "Remove"));

    card.append(top, actions);
    return card;
  }

  // 4. Event listeners
  // Show / hide the employee list
  toggleBtn.addEventListener("click", function () {
    const willShow = list.hidden;
    list.hidden = !willShow;
    toggleBtn.textContent = willShow ? "Hide Employees" : "Show Employees";
    toggleBtn.setAttribute("aria-expanded", String(willShow));
    updateStatus();
  });

  // Buttons inside employee cards (works for existing and newly added cards)
  list.addEventListener("click", function (event) {
    const button = event.target.closest("button[data-action]");
    if (!button) return;
    const card = button.closest(".emp-card");

    if (button.dataset.action === "remove") {
      card.remove();
    } else if (button.dataset.action === "toggle-status") {
      const nowActive = card.dataset.active !== "true";
      const pill = card.querySelector(".pill");
      card.dataset.active = String(nowActive);
      pill.textContent = nowActive ? "Active" : "Inactive";
      pill.className = nowActive ? "pill active" : "pill inactive";
      button.textContent = nowActive ? "Mark inactive" : "Mark active";
    }
    updateStatus();
  });

  // Update messages as the user corrects the input
  Object.keys(fields).forEach(function (key) {
    const recheck = function () {
      if (fields[key].input.getAttribute("aria-invalid") === "true") validateField(key);
      if (messages.classList.contains("success")) clearMessage();
      else if (messages.classList.contains("error") && !hasInvalidField()) clearMessage();
    };
    fields[key].input.addEventListener("input", recheck);
    fields[key].input.addEventListener("change", recheck);
  });

  // Submit: validate, then add the employee without reloading the page
  form.addEventListener("submit", function (event) {
    event.preventDefault();

    const keys = Object.keys(fields);
    const errors = keys.map(validateField).filter(Boolean);
    if (errors.length > 0) {
      showMessage("error", errors.length === 1 ? errors[0] : "Please correct the highlighted fields.");
      const firstInvalid = keys.find((key) => fields[key].input.getAttribute("aria-invalid") === "true");
      fields[firstInvalid].input.focus();
      return;
    }

    const employee = {
      name: fields.name.input.value.trim(),
      email: fields.email.input.value.trim(),
      department: fields.department.input.value,
      title: fields.title.input.value.trim(),
    };

    list.appendChild(createEmployeeCard(employee));
    form.reset();
    clearFieldErrors();
    showMessage("success", employee.name + " was added to the employee list.");
    updateStatus();
  });

  updateStatus();
})();