const menuButton = document.querySelector("[data-menu-toggle]");
const navigation = document.querySelector("[data-navigation]");
const navLinks = [...document.querySelectorAll('.primary-navigation a[href^="#"]')];
const sections = navLinks
  .map((link) => document.querySelector(link.getAttribute("href")))
  .filter(Boolean);

const closeMenu = () => {
  menuButton?.setAttribute("aria-expanded", "false");
  navigation?.removeAttribute("data-open");
};

menuButton?.addEventListener("click", () => {
  const open = menuButton.getAttribute("aria-expanded") === "true";
  menuButton.setAttribute("aria-expanded", String(!open));
  navigation?.toggleAttribute("data-open", !open);
});

navLinks.forEach((link) => link.addEventListener("click", closeMenu));

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && menuButton?.getAttribute("aria-expanded") === "true") {
    closeMenu();
    menuButton.focus();
  }
});

if ("IntersectionObserver" in window) {
  const observer = new IntersectionObserver(
    (entries) => {
      const visible = entries
        .filter((entry) => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
      if (!visible) return;
      navLinks.forEach((link) => {
        const active = link.getAttribute("href") === `#${visible.target.id}`;
        if (active) link.setAttribute("aria-current", "page");
        else link.removeAttribute("aria-current");
      });
    },
    { rootMargin: "-35% 0px -55%", threshold: [0, 0.25, 0.5] }
  );
  sections.forEach((section) => observer.observe(section));
}

const dialog = document.querySelector("[data-resource-dialog]");
let dialogTrigger = null;

document.querySelectorAll("[data-resource-open]").forEach((button) => {
  button.addEventListener("click", () => {
    dialogTrigger = button;
    dialog?.showModal();
  });
});

dialog?.querySelectorAll("[data-dialog-close]").forEach((button) => {
  button.addEventListener("click", () => dialog.close());
});

dialog?.addEventListener("click", (event) => {
  if (event.target === dialog) dialog.close();
});

dialog?.addEventListener("close", () => dialogTrigger?.focus());

document.querySelector("[data-brevo-pending]")?.addEventListener("submit", (event) => {
  event.preventDefault();
  const status = event.currentTarget.querySelector("[data-form-status]");
  if (status) {
    status.textContent =
      "La suscripción estará disponible cuando conectemos Sukum con Brevo.";
  }
});
