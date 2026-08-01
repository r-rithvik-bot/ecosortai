/* ==========================================================
   EcoSort AI — script.js
   Handles: AOS init, dark mode, animated counters,
   scroll-to-top, waste detection (AJAX), toasts, charts init.
   ========================================================== */

document.addEventListener("DOMContentLoaded", () => {
  initAOS();
  initDarkMode();
  initScrollTopButton();
  initCounters();
  initDetectPage();
  initUploadPreview();
});

/* ---------- AOS ---------- */
function initAOS() {
  if (window.AOS) {
    AOS.init({ duration: 700, once: true, offset: 60, easing: "ease-out-cubic" });
  }
}

/* ---------- Dark Mode ---------- */
function initDarkMode() {
  const toggleBtn = document.getElementById("darkModeToggle");
  if (!toggleBtn) return;

  const applyMode = (isDark) => {
    document.body.classList.toggle("dark-mode", isDark);
    toggleBtn.innerHTML = isDark
      ? '<i class="fa-solid fa-sun"></i>'
      : '<i class="fa-solid fa-moon"></i>';
  };

  // Note: uses in-memory state only (no localStorage per sandboxed environment best practice
  // fallback to a simple runtime variable). We still attempt localStorage gracefully.
  let savedPref = null;
  try { savedPref = localStorage.getItem("ecosort-theme"); } catch (e) { savedPref = null; }
  applyMode(savedPref === "dark");

  toggleBtn.addEventListener("click", () => {
    const isDark = !document.body.classList.contains("dark-mode");
    applyMode(isDark);
    try { localStorage.setItem("ecosort-theme", isDark ? "dark" : "light"); } catch (e) { /* ignore */ }
  });
}

/* ---------- Scroll to Top ---------- */
function initScrollTopButton() {
  const btn = document.getElementById("scrollTopBtn");
  if (!btn) return;
  window.addEventListener("scroll", () => {
    btn.classList.toggle("show", window.scrollY > 400);
  });
  btn.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));
}

/* ---------- Animated Counters ---------- */
function initCounters() {
  const counters = document.querySelectorAll("[data-counter]");
  if (!counters.length) return;

  const animate = (el) => {
    const target = parseFloat(el.getAttribute("data-counter"));
    const suffix = el.getAttribute("data-suffix") || "";
    const duration = 1600;
    const startTime = performance.now();

    const step = (now) => {
      const progress = Math.min((now - startTime) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const value = Math.floor(eased * target);
      el.textContent = value.toLocaleString() + suffix;
      if (progress < 1) requestAnimationFrame(step);
      else el.textContent = target.toLocaleString() + suffix;
    };
    requestAnimationFrame(step);
  };

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          animate(entry.target);
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.4 }
  );

  counters.forEach((c) => observer.observe(c));
}

/* ---------- Toast ---------- */
function showEcoToast(message, iconClass = "fa-circle-check") {
  let toast = document.getElementById("ecoToast");
  if (!toast) {
    toast = document.createElement("div");
    toast.id = "ecoToast";
    toast.className = "eco-toast";
    document.body.appendChild(toast);
  }
  toast.innerHTML = `<i class="fa-solid ${iconClass}"></i><span>${message}</span>`;
  requestAnimationFrame(() => toast.classList.add("show"));
  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => toast.classList.remove("show"), 3500);
}

/* ---------- Upload Preview (Detect Page) ---------- */
function initUploadPreview() {
  const fileInput = document.getElementById("wasteImage");
  const zone = document.getElementById("uploadZone");
  const preview = document.getElementById("previewImg");
  if (!fileInput || !zone) return;

  zone.addEventListener("click", () => fileInput.click());

  ["dragover", "dragenter"].forEach((evt) =>
    zone.addEventListener(evt, (e) => {
      e.preventDefault();
      zone.classList.add("dragover");
    })
  );
  ["dragleave", "drop"].forEach((evt) =>
    zone.addEventListener(evt, (e) => {
      e.preventDefault();
      zone.classList.remove("dragover");
    })
  );
  zone.addEventListener("drop", (e) => {
    if (e.dataTransfer.files.length) {
      fileInput.files = e.dataTransfer.files;
      showPreview(fileInput.files[0]);
    }
  });

  fileInput.addEventListener("change", () => {
    if (fileInput.files.length) showPreview(fileInput.files[0]);
  });

  function showPreview(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      preview.src = e.target.result;
      preview.style.display = "block";
    };
    reader.readAsDataURL(file);
  }
}

/* ---------- Detect Page: Identify Waste (simulated AI) ---------- */
function initDetectPage() {
  const form = document.getElementById("detectForm");
  if (!form) return;

  const binColorMap = {
    "Blue Bin": "#2f6fed",
    "Green Bin": "#2e9e5b",
    "Grey Bin": "#6b7280",
    "Brown Bin": "#8a5a2b",
    "Red Bin": "#d63b3b",
  };

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const select = document.getElementById("wasteType");
    const wasteType = select.value;
    if (!wasteType) {
      showEcoToast("Please choose a waste type first.", "fa-triangle-exclamation");
      return;
    }

    const resultCard = document.getElementById("resultCard");
    const spinner = document.getElementById("loadingSpinner");
    const submitBtn = document.getElementById("identifyBtn");

    resultCard.style.display = "none";
    spinner.style.display = "block";
    submitBtn.disabled = true;

    // Simulate AI "thinking" delay for realism
    await new Promise((res) => setTimeout(res, 1100));

    try {
      const response = await fetch("/api/identify", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ waste_type: wasteType }),
      });
      const data = await response.json();

      spinner.style.display = "none";
      submitBtn.disabled = false;

      if (!data.success) {
        showEcoToast(data.message || "Could not identify waste.", "fa-triangle-exclamation");
        return;
      }

      renderResult(data);
      showEcoToast(`+${data.points} EcoScore points earned!`, "fa-star");
    } catch (err) {
      spinner.style.display = "none";
      submitBtn.disabled = false;
      showEcoToast("Something went wrong. Please try again.", "fa-triangle-exclamation");
    }
  });

  function renderResult(data) {
    const resultCard = document.getElementById("resultCard");
    const color = binColorMap[data.bin_color] || "#2e9e5b";

    document.getElementById("resultHead").style.background =
      `linear-gradient(135deg, ${color}, ${shade(color, -20)})`;
    document.getElementById("resultIcon").innerHTML = `<i class="fa-solid ${data.icon}"></i>`;
    document.getElementById("resultLabel").textContent = data.label;
    document.getElementById("resultCategory").textContent = data.category;

    document.getElementById("valBin").textContent = data.bin_color;
    document.getElementById("valBin").style.color = color;
    document.getElementById("valRecyclable").textContent = data.recyclable;
    document.getElementById("valDisposal").textContent = data.disposal;
    document.getElementById("resultFact").textContent = data.fact;
    document.getElementById("resultPoints").textContent = `+${data.points} Points`;

    resultCard.style.display = "block";
    const placeholder = document.getElementById("placeholderCard");
    if (placeholder) placeholder.style.display = "none";
    resultCard.scrollIntoView({ behavior: "smooth", block: "center" });
  }

  function shade(hex, percent) {
    const num = parseInt(hex.replace("#", ""), 16);
    const amt = Math.round(2.55 * percent);
    const R = Math.min(255, Math.max(0, (num >> 16) + amt));
    const G = Math.min(255, Math.max(0, ((num >> 8) & 0x00ff) + amt));
    const B = Math.min(255, Math.max(0, (num & 0x0000ff) + amt));
    return `#${(0x1000000 + R * 0x10000 + G * 0x100 + B).toString(16).slice(1)}`;
  }
}
