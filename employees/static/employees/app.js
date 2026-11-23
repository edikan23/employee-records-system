// Dismiss flash messages
document.querySelectorAll("[data-dismiss]").forEach(b =>
  b.addEventListener("click", () => b.parentElement.remove()));

// Confirm before following delete links in the list
document.querySelectorAll("[data-confirm]").forEach(a =>
  a.addEventListener("click", e => { if (!confirm(a.dataset.confirm)) e.preventDefault(); }));

// Live search: submit the filter form shortly after typing stops or a filter changes
document.querySelectorAll("form[data-autosubmit]").forEach(form => {
  let t;
  const submit = () => form.requestSubmit();
  form.querySelector("input[type=search]").addEventListener("input", () => { clearTimeout(t); t = setTimeout(submit, 450); });
  form.querySelectorAll("select").forEach(s => s.addEventListener("change", submit));
  const box = form.querySelector("input[type=search]");
  if (box.value) { box.focus(); box.setSelectionRange(box.value.length, box.value.length); }
});

// Quick guide toggle
const guideBtn = document.getElementById("guide-toggle");
if (guideBtn) {
  const guideBody = document.getElementById("guide-body");
  guideBtn.addEventListener("click", () => {
    const opening = guideBody.hidden;
    guideBody.hidden = !opening;
    guideBtn.setAttribute("aria-expanded", String(opening));
    guideBtn.textContent = opening ? "Hide quick guide" : "Show quick guide";
  });
}