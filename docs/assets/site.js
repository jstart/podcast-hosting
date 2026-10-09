
document.querySelectorAll("[data-copy]").forEach((button) => {
  button.addEventListener("click", async () => {
    await navigator.clipboard.writeText(button.dataset.copy);
    const old = button.textContent;
    button.textContent = "Copied";
    setTimeout(() => { button.textContent = old; }, 1600);
  });
});

const isIOS = /^(iPhone|iPad|iPod)$/.test(navigator.platform)
  || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);

if (isIOS) {
  document.querySelectorAll("[data-pocket-casts-ios]").forEach((link) => {
    link.addEventListener("click", (event) => {
      if (event.defaultPrevented || event.button !== 0
          || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {
        return;
      }
      event.preventDefault();
      const fallback = link.href;
      const timer = setTimeout(() => {
        if (document.visibilityState === "visible") {
          window.location.assign(fallback);
        }
      }, 1200);
      window.addEventListener("pagehide", () => clearTimeout(timer), { once: true });
      window.location.assign(link.dataset.pocketCastsIos);
    });
  });
}
