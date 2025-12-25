(function () {
  function getCookie(name) {
    const m = document.cookie.match("(^|;)\\s*" + name + "\\s*=\\s*([^;]+)");
    return m ? decodeURIComponent(m.pop()) : "";
  }

  function translateUrl() {
    const p = window.location.pathname;
    return p.replace(/(add\/|[^/]+\/change\/)$/, "") + "translate/";
  }

  function isCkeditor(el) {
    return el && el.classList && el.classList.contains("django_ckeditor_5");
  }

  function getValue(fieldId) {
    const el = document.getElementById(fieldId);
    if (!el) return "";
    if (isCkeditor(el) && window.editors && window.editors[fieldId]) {
      return window.editors[fieldId].getData();
    }
    return el.value || "";
  }

  function setValue(fieldId, value) {
    const el = document.getElementById(fieldId);
    if (!el) return;
    if (isCkeditor(el) && window.editors && window.editors[fieldId]) {
      window.editors[fieldId].setData(value || "");
    }
    el.value = value || "";
    el.dispatchEvent(new Event("change"));
  }

  function ensureStatusEl(btn) {
    // создаём контейнер статуса рядом с кнопкой 1 раз
    let status = btn.parentNode.querySelector(".deepl-translate-status");
    if (!status) {
      status = document.createElement("span");
      status.className = "deepl-translate-status ml-2 text-sm";
      status.style.display = "inline-block";
      status.style.verticalAlign = "middle";
      btn.parentNode.appendChild(status);
    }
    return status;
  }

  function showStatus(btn, text, ok = true) {
    const status = ensureStatusEl(btn);
    status.textContent = text;
    status.classList.remove("text-red-600", "text-green-600");
    status.classList.add(ok ? "text-green-600" : "text-red-600");

    clearTimeout(status._t);
    status._t = setTimeout(() => {
      status.textContent = "";
      status.classList.remove("text-red-600", "text-green-600");
    }, ok ? 2500 : 5000);
  }

  function setBtnLoading(btn, isLoading) {
    btn.disabled = isLoading;
    btn.classList.toggle("opacity-60", isLoading);
    btn.classList.toggle("cursor-not-allowed", isLoading);
    btn.textContent = isLoading ? "Перевожу…" : "Перевести";
  }

  async function doTranslate(base, sourceLang, btn) {
    const langs = ["ru", "kk", "en"];
    const targets = langs.filter((l) => l !== sourceLang);

    const fieldId = `id_${base}_${sourceLang}`;
    const el = document.getElementById(fieldId);
    const text = getValue(fieldId);

    if (!text || !text.trim()) {
      showStatus(btn, "⚠️ Пустое поле", false);
      return;
    }

    const nonEmptyTargets = targets.filter(
      (t) => (getValue(`id_${base}_${t}`) || "").trim().length > 0
    );
    if (nonEmptyTargets.length && !confirm("Некоторые переводы уже заполнены. Перезаписать?")) {
      return;
    }

    setBtnLoading(btn, true);

    try {
      const resp = await fetch(translateUrl(), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
          base: base,
          source: sourceLang,
          targets: targets,
          text: text,
          is_html: isCkeditor(el),
        }),
      });

      if (!resp.ok) {
        const errText = await resp.text();
        showStatus(btn, `❌ Ошибка: ${resp.status}`, false);
        console.error("DeepL translate error:", resp.status, errText);
        return;
      }

      const data = await resp.json();
      const tr = data.translations || {};

      Object.keys(tr).forEach((t) => setValue(`id_${base}_${t}`, tr[t]));

      showStatus(btn, "✅ Переведено", true);
    } catch (e) {
      console.error(e);
      showStatus(btn, "❌ Ошибка сети", false);
    } finally {
      setBtnLoading(btn, false);
    }
  }

  function addButton(base, lang) {
    const fieldId = `id_${base}_${lang}`;
    const el = document.getElementById(fieldId);
    if (!el || el.dataset.translateBtnAdded === "1") return;

    const btn = document.createElement("button");
    btn.type = "button";

    // ваши классы (Unfold/Tailwind)
    btn.className =
      "bg-primary-600 block border border-transparent cursor-pointer font-medium px-3 py-2 rounded-default text-white w-full lg:w-auto";

    // чтобы не прилипало к полю (особенно если layout inline)
    btn.style.marginTop = "6px";

    btn.textContent = "Перевести";
    btn.addEventListener("click", () => doTranslate(base, lang, btn));

    el.parentNode.appendChild(btn);
    el.dataset.translateBtnAdded = "1";
  }

  document.addEventListener("DOMContentLoaded", () => {
    const bases = [
      "title",
      "summary",
      "customer",
      "location",
      "project_type",
      "task",
      "goal",
      "features",
      "role_in_project",
    ];
    const langs = ["ru", "kk", "en"];

    bases.forEach((base) => langs.forEach((lang) => addButton(base, lang)));
  });
})();
