(function () {
  function clamp01(v) { return Math.max(0, Math.min(1, v)); }

  function initWidget(root) {
    const img = root.querySelector(".image-point-img");
    const marker = root.querySelector(".image-point-marker");
    const input = root.querySelector(".image-point-input");
    const clearBtn = root.querySelector(".image-point-clear");

    function setPoint(x, y) {
      x = clamp01(x); y = clamp01(y);
      input.value = JSON.stringify({ x: +x.toFixed(6), y: +y.toFixed(6) });

      marker.hidden = false;
      marker.style.left = (x * 100) + "%";
      marker.style.top = (y * 100) + "%";
    }

    function clearPoint() {
      input.value = JSON.stringify({ x: null, y: null });
      marker.hidden = true;
    }

    img.addEventListener("click", (e) => {
      const rect = img.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width;
      const y = (e.clientY - rect.top) / rect.height;
      setPoint(x, y);
    });

    clearBtn.addEventListener("click", clearPoint);

    // initial
    const ix = root.dataset.initialX;
    const iy = root.dataset.initialY;
    if (ix !== "" && iy !== "") setPoint(parseFloat(ix), parseFloat(iy));
    else clearPoint();
  }

  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".image-point-widget").forEach(initWidget);
  });
})();
