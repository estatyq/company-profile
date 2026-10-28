(() => {
  "use strict";

  const bootNode = document.getElementById("admin-bootstrap");
  if (!bootNode) return;
  const boot = JSON.parse(bootNode.textContent);
  const csrf = boot.csrf;
  let content = boot.content;
  const languageCodes = boot.languages.map((language) => language.code);
  const languageNames = Object.fromEntries(
    boot.languages.map((language) => [language.code, language]),
  );
  const storedLanguage = localStorage.getItem(
    "company-profile-language-selection",
  );
  let activeLanguage = languageCodes.includes(storedLanguage)
    ? storedLanguage
    : "en";
  let dirty = false;
  let uploadedShots = new Map();

  const textGroups = [
    {
      title: "Главный экран",
      fields: [
        ["brand_submark", "Подпись рядом с логотипом"],
        ["cover_chip", "Плашка над заголовком"],
        ["cover_eyebrow", "Подпись в правом верхнем углу"],
        ["cover_products_label", "Подпись к продуктам"],
        ["cover_title_a", "Заголовок — первая строка"],
        ["cover_title_b", "Заголовок — акцентная строка"],
        ["cover_sub", "Подзаголовок", false, true],
        ["cover_lead", "Вводный текст", true],
        ["cover_cta_primary", "Главная кнопка"],
        ["cover_cta_secondary", "Вторая кнопка"],
        ["cover_trust", "Подпись под кнопками"],
      ],
    },
    {
      title: "О компании",
      fields: [
        ["p2_eyebrow", "Надзаголовок"],
        ["p2_problems_label", "Подпись к проблемам"],
        ["p2_flow_label", "Подпись к схеме"],
        ["p2_cmp_label", "Подпись к сравнению"],
        ["p2_title_a", "Заголовок — первая строка"],
        ["p2_title_b", "Заголовок — вторая строка"],
        ["p2_lead", "Описание", true],
      ],
    },
    {
      title: "Портфолио",
      fields: [
        ["p3_eyebrow", "Надзаголовок"],
        ["p3_title", "Заголовок"],
        ["p3_title_continued", "Заголовок продолжения"],
        ["p3_lead", "Описание", true],
        ["benefit_label", "Подпись к ценности проекта"],
      ],
    },
    {
      title: "Услуги",
      fields: [
        ["p4_eyebrow", "Надзаголовок"],
        ["p4_title", "Заголовок", false, true],
        ["p4_lead", "Описание", true],
        ["example_label", "Подпись к примерам"],
      ],
    },
    {
      title: "Преимущества",
      fields: [
        ["p5_eyebrow", "Надзаголовок"],
        ["p5_title_a", "Заголовок — первая строка"],
        ["p5_title_b", "Заголовок — вторая строка"],
        ["p5_lead", "Описание", true],
        ["p5_phases_label", "Подпись к этапам"],
      ],
    },
    {
      title: "Контакты",
      fields: [
        ["p6_eyebrow", "Надзаголовок"],
        ["p6_title", "Заголовок"],
        ["models_label", "Подпись к форматам работы"],
        ["cta_a", "Призыв к действию — первая фраза", true],
        ["cta_b", "Призыв к действию — акцент", true],
        ["cta_note", "Пояснение", true],
      ],
    },
  ];

  function clone(value) {
    return JSON.parse(JSON.stringify(value));
  }

  function escapeHtml(value = "") {
    return String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function imageUrl(shot) {
    if (!shot) return "";
    if (/^https?:\/\//i.test(shot) || shot.startsWith("data:")) return shot;
    return `/assets/web/${String(shot).replace(/^assets\/web\//, "")}`;
  }

  function markDirty() {
    dirty = true;
    const indicator = document.getElementById("save-indicator");
    const status = document.getElementById("save-status");
    indicator?.classList.add("dirty");
    if (status) status.textContent = "Есть несохранённые изменения";
  }

  function markClean(message = "Все изменения сохранены") {
    dirty = false;
    const indicator = document.getElementById("save-indicator");
    const status = document.getElementById("save-status");
    indicator?.classList.remove("dirty");
    if (status) status.textContent = message;
  }

  function showToast(message, isError = false) {
    const toast = document.getElementById("admin-toast");
    toast.textContent = message;
    toast.classList.toggle("error", isError);
    toast.classList.add("visible");
    clearTimeout(showToast.timer);
    showToast.timer = setTimeout(() => toast.classList.remove("visible"), 3400);
  }

  function fillIdentity() {
    document.getElementById("brand-field").value = content.brand || "";
    for (const kind of ["whatsapp", "telegram", "email", "website"]) {
      document.getElementById(`contact-${kind}`).value =
        content.contacts?.[kind] || "";
    }
    renderBrandLogoAdmin();
  }

  function renderBrandLogoAdmin() {
    const preview = document.getElementById("brand-logo-preview");
    if (!preview) return;
    const source = imageUrl(content.logo);
    preview.innerHTML = source
      ? `<img src="${escapeHtml(source)}" alt="Логотип ${escapeHtml(content.brand || "")}">`
      : "<span>Логотип не загружен</span>";
  }

  function collectIdentity() {
    content.brand = document.getElementById("brand-field").value.trim();
    content.contacts ||= {};
    for (const kind of ["whatsapp", "telegram", "email", "website"]) {
      content.contacts[kind] = document
        .getElementById(`contact-${kind}`)
        .value.trim();
    }
  }

  function renderLanguageTabs() {
    const host = document.querySelector(".language-switch");
    if (host) {
      host.innerHTML = boot.languages
        .map(
          (language) =>
            `<button type="button" data-language="${escapeHtml(language.code)}" aria-selected="false">${escapeHtml(language.native)}</button>`,
        )
        .join("");
      host.querySelectorAll("[data-language]").forEach((button) => {
        const active = button.dataset.language === activeLanguage;
        button.classList.toggle("active", active);
        button.setAttribute("aria-selected", String(active));
        button.addEventListener("click", () =>
          switchLanguage(button.dataset.language),
        );
      });
    }
    const label = document.getElementById("page-copy-language");
    if (label) {
      const native = languageNames[activeLanguage]?.native || activeLanguage;
      label.textContent = `Вы редактируете версию: ${native}.`;
    }
  }

  function renderTextFields() {
    const host = document.getElementById("text-fields");
    const current = content.languages[activeLanguage];
    host.innerHTML = textGroups
      .map(
        (group) => `
          <div class="text-group">
            <h3>${escapeHtml(group.title)}</h3>
            <div class="text-fields">
              ${group.fields
                .map(([key, label, multiline]) => {
                  const value = current.text?.[key] || "";
                  const wide = multiline ? " wide" : "";
                  return `<label class="text-field${wide}">
                    <span>${escapeHtml(label)}</span>
                    ${
                      multiline
                        ? `<textarea data-text-key="${key}" rows="3">${escapeHtml(value)}</textarea>`
                        : `<input data-text-key="${key}" type="text" maxlength="300" value="${escapeHtml(value)}">`
                    }
                  </label>`;
                })
                .join("")}
            </div>
          </div>`,
      )
      .join("");
  }

  function collectTextFields() {
    const current = content.languages[activeLanguage];
    current.text ||= {};
    document.querySelectorAll("[data-text-key]").forEach((field) => {
      current.text[field.dataset.textKey] = field.value;
    });
  }

  function renderProjects() {
    const host = document.getElementById("project-list");
    const projects = content.languages[activeLanguage].products || [];
    if (!projects.length) {
      host.innerHTML =
        '<p class="empty-projects">Пока нет проектов. Добавьте первую работу.</p>';
      return;
    }
    host.innerHTML = projects
      .map((project, index) => {
        const screenshot = imageUrl(project.shot);
        return `
          <details class="admin-project" data-project-id="${escapeHtml(project.id)}">
            <summary>
              <span class="project-number">${String(index + 1).padStart(2, "0")}</span>
              <span class="project-name">${escapeHtml(project.name || "Проект")}</span>
              <span class="project-chevron">⌄</span>
            </summary>
            <div class="project-body">
              <div class="field-grid">
                <label class="admin-field"><span>Название</span><input data-project-field="name" type="text" maxlength="80" value="${escapeHtml(project.name || "")}"></label>
                <label class="admin-field"><span>Статус</span><input data-project-field="status" type="text" maxlength="40" value="${escapeHtml(project.status || "")}"></label>
              </div>
              <label class="admin-field"><span>Ссылка на проект</span><input data-project-field="url" type="url" maxlength="500" value="${escapeHtml(project.url || "")}" placeholder="https://example.com"></label>
              <div class="field-grid">
                <label class="admin-field"><span>Короткая категория</span><input data-project-field="coverSub" type="text" maxlength="100" value="${escapeHtml(project.coverSub || "")}"></label>
                <label class="admin-field"><span>Описание проекта</span><input data-project-field="tag" type="text" maxlength="180" value="${escapeHtml(project.tag || "")}"></label>
              </div>
              <label class="admin-field"><span>Ключевые возможности — по одному пункту на строку</span><textarea data-project-field="features" rows="4">${escapeHtml((project.features || []).join("\n"))}</textarea></label>
              <label class="admin-field"><span>Ценность для клиента</span><textarea data-project-field="benefit" rows="3" maxlength="500">${escapeHtml(project.benefit || "")}</textarea></label>
              <div class="project-media">
                <div class="project-thumb">${
                  screenshot
                    ? `<img src="${escapeHtml(screenshot)}" alt="">`
                    : "Нет скриншота"
                }</div>
                <div>
                  <b>Скриншот проекта</b>
                  <p>JPG, PNG или WebP до 10 МБ. Сервер уменьшит изображение автоматически.</p>
                  <label class="upload-label">
                    ${screenshot ? "Заменить изображение" : "Загрузить изображение"}
                    <input type="file" accept="image/jpeg,image/png,image/webp" data-upload-image hidden>
                  </label>
                </div>
              </div>
              <div class="project-actions">
                <button class="delete-project" type="button" data-delete-project>Удалить проект</button>
              </div>
            </div>
          </details>`;
      })
      .join("");
  }

  function collectProjects() {
    const projects = [];
    document.querySelectorAll(".admin-project").forEach((node) => {
      const id = node.dataset.projectId;
      const previous = content.languages[activeLanguage].products.find(
        (project) => project.id === id,
      ) || { id, badgeColor: "r" };
      const get = (name) =>
        node.querySelector(`[data-project-field="${name}"]`)?.value || "";
      projects.push({
        ...previous,
        id,
        name: get("name").trim(),
        url: get("url").trim(),
        shot: uploadedShots.get(id) || previous.shot || "",
        coverSub: get("coverSub").trim(),
        status: get("status").trim(),
        tag: get("tag").trim(),
        features: get("features")
          .split("\n")
          .map((line) => line.trim())
          .filter(Boolean),
        benefit: get("benefit").trim(),
      });
    });
    content.languages[activeLanguage].products = projects;
  }

  function syncVisibleState() {
    collectIdentity();
    collectTextFields();
    collectProjects();
  }

  function syncCommonProjectFields(sourceLanguage) {
    const source = content.languages[sourceLanguage]?.products || [];
    const common = new Map(source.map((project) => [project.id, project]));
    for (const lang of languageCodes) {
      for (const project of content.languages[lang].products || []) {
        const sourceProject = common.get(project.id);
        if (!sourceProject) continue;
        for (const key of ["name", "url", "shot", "status", "coverSub"]) {
          project[key] = sourceProject[key] || "";
        }
      }
    }
  }

  function switchLanguage(language) {
    if (language === activeLanguage) return;
    const previousLanguage = activeLanguage;
    syncVisibleState();
    syncCommonProjectFields(previousLanguage);
    activeLanguage = language;
    localStorage.setItem("company-profile-language-selection", language);
    renderLanguageTabs();
    renderTextFields();
    renderProjects();
  }

  function addProject() {
    syncVisibleState();
    const id = `project-${Date.now().toString(36)}-${Math.random()
      .toString(36)
      .slice(2, 7)}`;
    for (const lang of languageCodes) {
      content.languages[lang].products.push({
        id,
        name:
          lang === "uk"
            ? "Новий проєкт"
            : lang === "de"
              ? "Neues Projekt"
              : lang === "es"
                ? "Nuevo proyecto"
                : lang === "id"
                  ? "Proyek baru"
                  : "New project",
        url: "",
        shot: "",
        coverSub: "",
        status: lang === "id" ? "Aktif" : lang === "uk" ? "Активний" : lang === "es" ? "Activo" : "Live",
        tag: "",
        features: [],
        benefit: "",
        badgeColor: ["r", "m", "f"][
          content.languages[lang].products.length % 3
        ],
      });
    }
    markDirty();
    renderProjects();
    const project = Array.from(document.querySelectorAll(".admin-project")).at(-1);
    if (project) {
      project.open = true;
      project.scrollIntoView({ behavior: "smooth", block: "center" });
      project.querySelector('[data-project-field="name"]')?.focus();
    }
  }

  function deleteProject(id) {
    if (!window.confirm("Удалить этот проект из обеих языковых версий?")) return;
    syncVisibleState();
    for (const lang of languageCodes) {
      content.languages[lang].products = content.languages[lang].products.filter(
        (project) => project.id !== id,
      );
    }
    uploadedShots.delete(id);
    markDirty();
    renderProjects();
  }

  async function uploadImage(projectNode, file) {
    const id = projectNode.dataset.projectId;
    const form = new FormData();
    form.append("image", file);
    const upload = projectNode.querySelector("[data-upload-image]");
    upload.disabled = true;
    try {
      const response = await fetch("/api/admin/upload", {
        method: "POST",
        headers: { "X-CSRF-Token": csrf },
        body: form,
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(data.error || "Не удалось загрузить изображение.");
      uploadedShots.set(id, data.shot);
      const preview = projectNode.querySelector(".project-thumb");
      preview.innerHTML = `<img src="${escapeHtml(imageUrl(data.shot))}" alt="">`;
      markDirty();
      showToast("Скриншот загружен");
    } catch (error) {
      showToast(error.message || "Ошибка загрузки", true);
    } finally {
      upload.disabled = false;
      upload.value = "";
    }
  }

  async function uploadBrandLogo(file) {
    const input = document.getElementById("brand-logo-file");
    const form = new FormData();
    form.append("logo", file);
    input.disabled = true;
    try {
      const response = await fetch("/api/admin/logo", {
        method: "POST",
        headers: { "X-CSRF-Token": csrf },
        body: form,
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(data.error || "Не удалось загрузить логотип.");
      content.logo = data.logo;
      renderBrandLogoAdmin();
      markDirty();
      showToast("Логотип загружен");
    } catch (error) {
      showToast(error.message || "Ошибка загрузки логотипа", true);
    } finally {
      input.disabled = false;
      input.value = "";
    }
  }

  async function saveContent() {
    const button = document.getElementById("save-content");
    syncVisibleState();
    syncCommonProjectFields(activeLanguage);
    button.disabled = true;
    button.textContent = "Сохраняем…";
    try {
      const response = await fetch("/api/admin/content", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "X-CSRF-Token": csrf,
        },
        body: JSON.stringify(content),
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(data.error || "Не удалось сохранить изменения.");
      content = data.content;
      uploadedShots = new Map();
      fillIdentity();
      renderTextFields();
      renderProjects();
      markClean();
      showToast("Изменения опубликованы");
    } catch (error) {
      showToast(error.message || "Ошибка сохранения", true);
      markDirty();
    } finally {
      button.disabled = false;
      button.textContent = "Сохранить изменения";
    }
  }

  async function changePassword(event) {
    event.preventDefault();
    const form = event.currentTarget;
    const formData = new FormData(form);
    if (formData.get("new_password") !== formData.get("confirmation")) {
      showToast("Новые пароли не совпадают.", true);
      return;
    }
    const button = form.querySelector('button[type="submit"]');
    button.disabled = true;
    try {
      const response = await fetch("/api/admin/password", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRF-Token": csrf,
        },
        body: JSON.stringify({
          current: formData.get("current"),
          new: formData.get("new_password"),
        }),
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(data.error || "Не удалось изменить пароль.");
      form.reset();
      showToast("Пароль обновлён");
    } catch (error) {
      showToast(error.message || "Ошибка смены пароля", true);
    } finally {
      button.disabled = false;
    }
  }

  function bindEvents() {
    document.getElementById("admin-form")?.addEventListener("input", markDirty);
    document.getElementById("admin-form")?.addEventListener("change", markDirty);
    document.getElementById("add-project")?.addEventListener("click", addProject);
    document
      .getElementById("save-content")
      ?.addEventListener("click", saveContent);
    document
      .getElementById("project-list")
      ?.addEventListener("click", (event) => {
        const button = event.target.closest("[data-delete-project]");
        if (!button) return;
        const project = button.closest(".admin-project");
        if (project) deleteProject(project.dataset.projectId);
      });
    document
      .getElementById("project-list")
      ?.addEventListener("change", async (event) => {
        if (!event.target.matches("[data-upload-image]")) return;
        const file = event.target.files?.[0];
        const project = event.target.closest(".admin-project");
        if (file && project) await uploadImage(project, file);
      });
    document
      .getElementById("brand-logo-file")
      ?.addEventListener("change", async (event) => {
        const file = event.target.files?.[0];
        if (file) await uploadBrandLogo(file);
      });
    document
      .getElementById("remove-brand-logo")
      ?.addEventListener("click", () => {
        content.logo = "";
        renderBrandLogoAdmin();
        markDirty();
      });
    document.getElementById("password-form")?.addEventListener("submit", changePassword);
    window.addEventListener("beforeunload", (event) => {
      if (!dirty) return;
      event.preventDefault();
      event.returnValue = "";
    });
    document.querySelectorAll(".admin-sidebar nav a").forEach((link) => {
      link.addEventListener("click", () => {
        document
          .querySelectorAll(".admin-sidebar nav a")
          .forEach((item) => item.classList.remove("active"));
        link.classList.add("active");
      });
    });
  }

  function initPasswordPanel() {
    if (!boot.environmentPassword) return;
    const panel = document.getElementById("password-panel");
    panel.innerHTML =
      "<summary>Пароль управляется настройками сервера</summary><p class=\"protected-password-note\">Смена через панель отключена. Пароль задаётся переменной окружения <code>ADMIN_PASSWORD</code>.</p>";
  }

  function init() {
    fillIdentity();
    renderLanguageTabs();
    renderTextFields();
    renderProjects();
    bindEvents();
    initPasswordPanel();
    markClean();
  }

  init();
})();
