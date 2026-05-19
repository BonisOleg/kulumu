/**
 * lazy_images.js — IntersectionObserver фолбек для lazy loading
 * Для браузерів де не підтримується loading="lazy"
 */

export function initLazy() {
  if ("loading" in HTMLImageElement.prototype) {
    // Браузер підтримує нативний lazy — нічого не робимо
    return;
  }

  const lazyImages = document.querySelectorAll("img[data-src]");
  if (!lazyImages.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const img = entry.target;
        img.src = img.dataset.src;
        if (img.dataset.srcset) {
          img.srcset = img.dataset.srcset;
        }
        img.removeAttribute("data-src");
        observer.unobserve(img);
      }
    });
  }, { rootMargin: "200px 0px" });

  lazyImages.forEach((img) => observer.observe(img));
}
