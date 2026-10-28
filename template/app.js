(() => {
  "use strict";

  const STORAGE_KEY = "company-profile-builder-v1";
  const LANGUAGE_KEY = "company-profile-language-selection";
  const MAX_PRODUCTS_PER_PAGE = 3;
  const configNode = document.getElementById("profile-config");
  if (!configNode) return;

  const baseConfig = JSON.parse(configNode.textContent);
  const serverMode = ["http:", "https:"].includes(window.location.protocol);
  let store = serverMode ? {} : readStore();
  let profile = mergeProfile(baseConfig, store);
  let draft = clone(profile);
  let draftImages = new Map();
  let editorOpen = false;

  const icons = {
    tick: '<polyline points="20 6 9 17 4 12"/>',
    out: '<path d="M7 17 17 7"/><path d="M7 7h10v10"/>',
    whatsapp:
      '<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>',
    telegram: '<path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4 20-7z"/>',
    email:
      '<rect x="2" y="4" width="20" height="16" rx="2"/><polyline points="22,6 12,13 2,6"/>',
    website:
      '<circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
  };

  const ui = {
    title: "Редактор профиля",
    intro:
      "Измените название, контакты и портфолио. После сохранения обновится сайт и оба экспорта.",
    identity: "Название и контакты",
    brand: "Название студии или ваше имя",
    brandHint: "Показывается в шапке сайта и документах.",
    contacts: "Контакты",
    whatsapp: "WhatsApp",
    telegram: "Telegram",
    email: "Email",
    website: "Сайт",
    portfolio: "Портфолио",
    portfolioHint:
      "Скриншоты автоматически сжимаются. Портфолио раскладывается на дополнительные слайды.",
    addProject: "Добавить проект",
    project: "Проект",
    name: "Название",
    url: "Ссылка",
    category: "Короткая категория",
    status: "Статус",
    tag: "Подпись проекта",
    description: "Описание",
    features: "Ключевые возможности",
    featuresHint: "Каждый пункт — с новой строки.",
    benefit: "Ценность для клиента",
    screenshot: "Скриншот",
    upload: "Загрузить изображение",
    replaceImage: "Заменить изображение",
    delete: "Удалить",
    backup: "Резервная копия",
    exportJson: "Скачать данные",
    importJson: "Загрузить данные",
    cancel: "Отмена",
    save: "Сохранить",
    reset: "Сбросить изменения",
    saved: "Профиль сохранён в этом браузере",
    resetConfirm: "Вернуть исходные название, контакты и проекты?",
    deleteConfirm: "Удалить этот проект из портфолио?",
    empty: "Нажмите «Добавить проект», чтобы показать первую работу.",
    storageError:
      "Не удалось сохранить: браузеру не хватает места. Уменьшите размер скриншотов или скачайте резервную копию.",
    importError: "Не удалось прочитать файл. Выберите JSON, созданный этим редактором.",
    imported: "Данные загружены. Проверьте изменения и нажмите «Сохранить».",
  };

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

  function svg(name, cls = "") {
    return `<svg class="${cls}" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">${icons[name] || ""}</svg>`;
  }

  function readStore() {
    try {
      const parsed = JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
      return parsed && typeof parsed === "object" ? parsed : {};
    } catch {
      return {};
    }
  }

  function mergeProfile(defaults, savedStore, published = {}) {
    const language = defaults.lang;
    const savedLanguage = savedStore.languages?.[language] || {};
    const products = Array.isArray(savedLanguage.products)
      ? savedLanguage.products
      : Array.isArray(published.products)
        ? published.products
        : clone(defaults.products);
    return {
      ...clone(defaults),
      text: {
        ...clone(defaults.text),
        ...(published.text && typeof published.text === "object"
          ? published.text
          : {}),
        ...(savedLanguage.text && typeof savedLanguage.text === "object"
          ? savedLanguage.text
          : {}),
      },
      brand:
        typeof savedStore.brand === "string"
          ? savedStore.brand
          : typeof published.brand === "string"
            ? published.brand
            : defaults.brand,
      logo:
        typeof published.logo === "string"
          ? published.logo
          : defaults.logo || "",
      contacts: {
        ...defaults.contacts,
        ...(published.contacts && typeof published.contacts === "object"
          ? published.contacts
          : {}),
        ...(savedStore.contacts && typeof savedStore.contacts === "object"
          ? savedStore.contacts
          : {}),
      },
      products,
    };
  }

  function persistProfile(nextProfile) {
    store.brand = nextProfile.brand;
    store.contacts = nextProfile.contacts;
    store.languages ||= {};
    store.languages[nextProfile.lang] = {
      products: nextProfile.products,
      text: nextProfile.text,
    };
    store.version = 1;
    localStorage.setItem(STORAGE_KEY, JSON.stringify(store));
  }

  function normalizeUrl(value) {
    const clean = String(value || "").trim();
    if (!clean) return "";
    if (/^(https?:|mailto:|tel:)/i.test(clean)) return clean;
    return `https://${clean}`;
  }

  function host(value) {
    return String(value || "")
      .replace(/^https?:\/\//i, "")
      .replace(/\/+$/, "");
  }

  function contactHref(kind, value) {
    const clean = String(value || "").trim();
    if (!clean) return "";
    if (kind === "whatsapp") {
      return `https://wa.me/${clean.replace(/\D/g, "")}`;
    }
    if (kind === "telegram") {
      return `https://t.me/${clean
        .replace(/^https?:\/\/(t\.me|telegram\.me)\//i, "")
        .replace(/^@/, "")}`;
    }
    if (kind === "email") return `mailto:${clean}`;
    return normalizeUrl(clean);
  }

  function imageSource(product) {
    if (product.imageData) return product.imageData;
    if (product.shot) return `assets/web/${product.shot}`;
    return "";
  }

  function logoSource(path) {
    if (!path) return "";
    if (/^(https?:|data:|blob:)/i.test(path)) return path;
    return `assets/web/${String(path).replace(/^assets\/web\//, "")}`;
  }

  function productCard(product, text) {
    const url = normalizeUrl(product.url);
    const screenshot = imageSource(product);
    const features = (product.features || [])
      .map((feature) => String(feature || "").trim())
      .filter(Boolean);
    const media = screenshot
      ? `<img src="${escapeHtml(screenshot)}" alt="${escapeHtml(product.name)}">`
      : `<div class="portfolio-placeholder">${escapeHtml(product.name || "Project")}</div>`;
    const shot = url
      ? `<a class="shot" href="${escapeHtml(url)}" target="_blank" rel="noopener">${media}<span class="status"><i></i>${escapeHtml(product.status || "Live")}</span></a>`
      : `<div class="shot">${media}<span class="status"><i></i>${escapeHtml(product.status || "Live")}</span></div>`;
    const projectLink = url
      ? `<a class="product-action" href="${escapeHtml(url)}" target="_blank" rel="noopener">${escapeHtml(
          product.actionLabel || text.ui_open_product || "Open product",
        )}${svg("out")}</a>`
      : "";
    return `
      <div class="card prod">
        ${shot}
        <div class="info">
          <div class="name"><b>${escapeHtml(product.name || "Project")}</b>${projectLink}</div>
          <div class="tag">${escapeHtml(product.tag || product.coverSub || "")}</div>
          <ul>${features
            .map((feature) => `<li>${svg("tick")}<span>${escapeHtml(feature)}</span></li>`)
            .join("")}</ul>
          ${
            product.benefit
              ? `<div class="benefit"><span class="label">${escapeHtml(
                  text.benefit_label || "Business value",
                )}</span>${escapeHtml(product.benefit)}</div>`
              : ""
          }
        </div>
      </div>`;
  }

  function coverPill(product) {
    const url = normalizeUrl(product.url);
    const color = ["r", "m", "f"].includes(product.badgeColor)
      ? product.badgeColor
      : "r";
    const subtitle = [product.coverSub, host(url)].filter(Boolean).join(" · ");
    const tag = url ? "a" : "div";
    const href = url ? ` href="${escapeHtml(url)}" target="_blank" rel="noopener"` : "";
    return `<${tag} class="pill"${href}><span class="pm ${color}">${escapeHtml(
      (product.name || "P").slice(0, 1).toUpperCase(),
    )}</span><span><b>${escapeHtml(product.name || "Project")}</b><small>${escapeHtml(
      subtitle,
    )}</small></span>${svg("out")}</${tag}>`;
  }

  function coverMorePill(count, text) {
    return `<a class="pill pill-more" href="#products"><span class="pm">+${count}</span><span><b>${escapeHtml(
      text.ui_more_projects || "More projects",
    )}</b><small>${escapeHtml(
      text.ui_view_portfolio || "View portfolio",
    )}</small></span>${svg("out")}</a>`;
  }

  function contactRow(kind, value, text) {
    if (!String(value || "").trim()) return "";
    const labels = text.contact_labels || {};
    const placeholders = text.contact_placeholders || {};
    const href = contactHref(kind, value);
    const tag = href ? "a" : "div";
    const link = href
      ? ` href="${escapeHtml(href)}" target="_blank" rel="noopener"`
      : "";
    return `<${tag} class="contact"${link}><div class="ci">${svg(
      kind,
    )}</div><div><small>${escapeHtml(
      labels[kind] || kind,
    )}</small><b class="${value ? "" : "ph"}">${escapeHtml(
      value || placeholders[kind] || "",
    )}</b></div></${tag}>`;
  }

  function renderProfile(nextProfile) {
    profile = nextProfile;
    const brand = profile.brand?.trim() || profile.descriptor;
    const studioLabel = profile.text?.brand_submark || profile.docLabel;
    const webTitle = studioLabel
      ? studioLabel.charAt(0).toUpperCase() + studioLabel.slice(1)
      : profile.docLabel;
    document
      .querySelectorAll(
        ".mark .brand-name, .mark > span:not(.submark), .language-gate-brand > span",
      )
      .forEach((node) => {
        node.textContent = brand;
      });
    document.title = `${brand} — ${webTitle}`;
    renderBrandLogo(profile.logo);
    updateSeoMetadata(brand);

    renderEditableText();
    const coverRow = document.querySelector(".cover .products .row");
    if (coverRow) {
      const visibleProducts = profile.products.slice(0, 3);
      const remaining = profile.products.length - visibleProducts.length;
      coverRow.innerHTML =
        visibleProducts.map(coverPill).join("") +
        (remaining
          ? coverMorePill(remaining, profile.text || {})
          : "");
    }
    renderPortfolioPages();
    renderContacts();
    renderFooters();
    renumberPages();
    updateWhatsAppButton();
    rescaleDeck();
  }

  function renderBrandLogo(path) {
    const source = logoSource(path);
    document.querySelectorAll(".mark, .language-gate-brand").forEach((host) => {
      let image = host.querySelector(".brand-logo");
      if (!source) return;
      if (!image) {
        image = document.createElement("img");
        image.className = "brand-logo";
        image.alt = "";
        const svg = host.querySelector("svg");
        if (svg) svg.replaceWith(image);
        else host.prepend(image);
      }
      image.src = source;
    });
    if (source) {
      const icon = document.querySelector('link[rel="icon"]');
      if (icon) icon.href = source;
    }
  }

  function updateSeoMetadata(brand) {
    const description = profile.text?.cover_lead || "";
    const values = {
      "meta[name='description']": description,
      "meta[property='og:site_name']": brand,
      "meta[property='og:description']": description,
      "meta[name='twitter:description']": description,
      "meta[property='og:title']": `${brand} — ${profile.text?.brand_submark || profile.docLabel}`,
      "meta[name='twitter:title']": `${brand} — ${profile.text?.brand_submark || profile.docLabel}`,
    };
    Object.entries(values).forEach(([selector, value]) => {
      const node = document.querySelector(selector);
      if (node && value) node.setAttribute("content", value);
    });
    const schemaNode = document.getElementById("organization-schema");
    if (!schemaNode) return;
    try {
      const schema = JSON.parse(schemaNode.textContent);
      schema.name = brand;
      schema.description = description;
      if (profile.logo) {
        schema.logo = new URL(logoSource(profile.logo), window.location.href).href;
      }
      schemaNode.textContent = JSON.stringify(schema);
    } catch {
      // Keep the static structured data if an administrator supplies odd content.
    }
  }

  function renderEditableText() {
    const text = profile.text || {};
    const setText = (selector, value) => {
      const node = document.querySelector(selector);
      if (node && typeof value === "string") node.textContent = value;
    };
    const setEyebrow = (selector, value) => {
      const node = document.querySelector(selector);
      if (node && typeof value === "string") {
        node.innerHTML = `<span class="dot"></span>${escapeHtml(value)}`;
      }
    };

    setText(".mark .submark", text.brand_submark);
    const coverChip = document.querySelector(".cover .chip");
    if (coverChip && typeof text.cover_chip === "string") {
      coverChip.innerHTML = `<span class="dot"></span>${escapeHtml(text.cover_chip)}`;
    }
    setText(".cover [data-cover-eyebrow]", text.cover_eyebrow);
    const coverTitle = document.querySelector(".cover .h1");
    if (coverTitle && text.cover_title_a && text.cover_title_b) {
      coverTitle.innerHTML = `${escapeHtml(text.cover_title_a)}<br><span class="grad">${escapeHtml(text.cover_title_b)}</span>`;
      coverTitle.classList.toggle(
        "long",
        (text.cover_title_a + text.cover_title_b).length > 44,
      );
    }
    setText(".cover .sub", text.cover_sub);
    setText(".cover .lead", text.cover_lead);
    setText(".cover .products > .label", text.cover_products_label);
    setText(".cover [data-cover-cta-primary]", text.cover_cta_primary);
    setText(".cover [data-cover-cta-secondary]", text.cover_cta_secondary);
    setText(".cover [data-cover-trust]", text.cover_trust);

    setEyebrow(".p2 .top .eyebrow", text.p2_eyebrow);
    const aboutTitle = document.querySelector(".p2 .head h2");
    if (aboutTitle && text.p2_title_a && text.p2_title_b) {
      aboutTitle.innerHTML = `${escapeHtml(text.p2_title_a)}<br><span class="grad">${escapeHtml(text.p2_title_b)}</span>`;
    }
    setText(".p2 .head .lead", text.p2_lead);
    setText(".p2 .problems > .label", text.p2_problems_label);
    setText(".p2 .flowcard > .label", text.p2_flow_label);
    setText(".p2 .cmpcard > .label", text.p2_cmp_label);

    setEyebrow(".p4 .top .eyebrow", text.p4_eyebrow);
    setText(".p4 .head h2", text.p4_title);
    setText(".p4 .head .lead", text.p4_lead);
    document.querySelectorAll(".p4 .svc .ex b").forEach((node) => {
      if (text.example_label) node.textContent = text.example_label;
    });

    setEyebrow(".p5 .top .eyebrow", text.p5_eyebrow);
    const whyTitle = document.querySelector(".p5 .leftcol h2");
    if (whyTitle && text.p5_title_a && text.p5_title_b) {
      whyTitle.innerHTML = `${escapeHtml(text.p5_title_a)}<br><span class="grad">${escapeHtml(text.p5_title_b)}</span>`;
    }
    setText(".p5 .leftcol .lead", text.p5_lead);
    setText(".p5 .phases > .label", text.p5_phases_label);

    setEyebrow(".p6 .top .eyebrow", text.p6_eyebrow);
    setText(".p6 .title h2", text.p6_title);
    setText(".p6 .models > .label", text.models_label);
    const cta = document.querySelector(".p6 .cta .q");
    if (cta && typeof text.cta_a === "string" && typeof text.cta_b === "string") {
      cta.innerHTML = `${escapeHtml(text.cta_a)} <span class="grad">${escapeHtml(text.cta_b)}</span>`;
    }
    setText(".p6 .cta .note", text.cta_note);
  }

  function renderPortfolioPages() {
    const firstPage = document.querySelector("[data-product-page]");
    if (!firstPage) return;
    document
      .querySelectorAll("[data-product-page]")
      .forEach((page, index) => {
        if (index > 0) page.remove();
      });

    const products = profile.products || [];
    const chunks = balancedChunks(products, MAX_PRODUCTS_PER_PAGE);

    let previous = firstPage;
    chunks.forEach((chunk, index) => {
      const page = index === 0 ? firstPage : firstPage.cloneNode(true);
      if (index > 0) previous.after(page);
      previous = page;
      page.dataset.productPage = String(index);
      if (index === 0) page.id = "products";
      else page.removeAttribute("id");

      const eyebrow = page.querySelector(".top .eyebrow");
      if (eyebrow) {
        portraitEyebrow(eyebrow, profile.text.p3_eyebrow, index);
      }
      const heading = page.querySelector(".head h2");
      if (heading) {
        heading.textContent =
          index === 0
            ? profile.text.p3_title
            : profile.text.p3_title_continued || profile.text.p3_title;
      }
      const cards = page.querySelector(".cards");
      if (cards) {
        const columns = Math.max(1, chunk.length);
        cards.style.gridTemplateColumns = `repeat(${columns}, minmax(0, 1fr))`;
        cards.innerHTML = chunk.length
          ? chunk.map((product) => productCard(product, profile.text)).join("")
          : `<div class="portfolio-empty"><b>${escapeHtml(
              profile.text.p3_title || "Portfolio",
            )}</b><span>${escapeHtml(ui.empty)}</span></div>`;
      }
    });
  }

  function portraitEyebrow(node, text, index) {
    node.innerHTML = `<span class="dot"></span>${escapeHtml(
      text + (index ? ` · ${index + 1}` : ""),
    )}`;
  }

  function balancedChunks(items, pageSize) {
    if (!items.length) return [[]];
    const pageCount = Math.ceil(items.length / pageSize);
    const baseSize = Math.floor(items.length / pageCount);
    const extra = items.length % pageCount;
    const chunks = [];
    let cursor = 0;
    for (let index = 0; index < pageCount; index += 1) {
      const size = baseSize + (index < extra ? 1 : 0);
      chunks.push(items.slice(cursor, cursor + size));
      cursor += size;
    }
    return chunks;
  }

  function renderContacts() {
    const contacts = document.querySelector(".p6 .contacts");
    if (!contacts) return;
    contacts.innerHTML = ["whatsapp", "telegram", "email", "website"]
      .map((kind) =>
        contactRow(kind, profile.contacts?.[kind] || "", profile.text),
      )
      .join("");
  }

  function footerLinks() {
    const shown = (profile.products || []).slice(0, 4);
    let html = shown
      .map((product) => {
        const url = normalizeUrl(product.url);
        return url
          ? `<a href="${escapeHtml(url)}" target="_blank" rel="noopener">${escapeHtml(
              host(url),
            )}</a>`
          : "";
      })
      .join("");
    const hidden = (profile.products || []).length - shown.length;
    if (hidden > 0) html += `<span class="links-more">+${hidden}</span>`;
    return html;
  }

  function renderFooters() {
    document.querySelectorAll(".foot .links").forEach((node) => {
      node.innerHTML = footerLinks();
    });
  }

  function renumberPages() {
    const pages = Array.from(document.querySelectorAll(".deck-container .page"));
    pages.forEach((page, index) => {
      const number = page.querySelector(".foot .num");
      if (number) number.textContent = `${String(index + 1).padStart(2, "0")} / ${String(pages.length).padStart(2, "0")}`;
    });
  }

  function updateWhatsAppButton() {
    const button = document.getElementById("whatsapp-cta");
    if (!button) return;
    const href = contactHref("whatsapp", profile.contacts?.whatsapp);
    button.hidden = !href;
    if (href) button.href = href;
  }

  function rescaleDeck() {
    if (typeof window.rescaleProfileDeck === "function") {
      window.rescaleProfileDeck();
      return;
    }
    const width = window.innerWidth;
    const pages = document.querySelectorAll(".deck-container .page");
    if (width >= 1320) {
      pages.forEach((page) => {
        page.style.transform = "none";
        page.style.marginBottom = "0";
      });
      return;
    }
    const scale = (width - (width < 768 ? 24 : 32)) / 1280;
    pages.forEach((page) => {
      page.style.transform = `scale(${scale})`;
      page.style.marginBottom = `${-(720 * (1 - scale))}px`;
    });
  }

  function openEditor() {
    if (editorOpen) return;
    editorOpen = true;
    draft = clone(profile);
    draftImages = new Map(
      (draft.products || [])
        .filter((product) => product.imageData)
        .map((product) => [product.id, product.imageData]),
    );
    renderProductEditors();
    fillIdentityFields();
    document.getElementById("profile-editor").hidden = false;
    document.body.classList.add("editor-is-open");
    requestAnimationFrame(() => {
      const panel = document.querySelector(".editor-panel");
      panel?.focus();
    });
  }

  function closeEditor() {
    if (!editorOpen) return;
    editorOpen = false;
    document.getElementById("profile-editor").hidden = true;
    document.body.classList.remove("editor-is-open");
    document.getElementById("edit-profile")?.focus();
  }

  function fillIdentityFields() {
    document.getElementById("editor-brand").value = draft.brand || "";
    for (const kind of ["whatsapp", "telegram", "email", "website"]) {
      document.getElementById(`editor-${kind}`).value =
        draft.contacts?.[kind] || "";
    }
  }

  function collectIdentity() {
    const contacts = {};
    for (const kind of ["whatsapp", "telegram", "email", "website"]) {
      contacts[kind] = document.getElementById(`editor-${kind}`).value.trim();
    }
    return {
      brand: document.getElementById("editor-brand").value.trim(),
      contacts,
    };
  }

  function collectProductsFromEditor() {
    return Array.from(document.querySelectorAll(".product-editor")).map(
      (node) => {
        const id = node.dataset.productId;
        const original =
          draft.products.find((product) => product.id === id) || {};
        return {
          ...original,
          id,
          name: node.querySelector('[data-field="name"]').value.trim(),
          url: node.querySelector('[data-field="url"]').value.trim(),
          coverSub: node
            .querySelector('[data-field="coverSub"]')
            .value.trim(),
          status: node
            .querySelector('[data-field="status"]')
            .value.trim(),
          tag: node.querySelector('[data-field="tag"]').value.trim(),
          features: node
            .querySelector('[data-field="features"]')
            .value.split("\n")
            .map((line) => line.trim())
            .filter(Boolean),
          benefit: node
            .querySelector('[data-field="benefit"]')
            .value.trim(),
          imageData: draftImages.get(id) || original.imageData || "",
        };
      },
    );
  }

  function refreshDraftFromForms() {
    Object.assign(draft, collectIdentity());
    draft.products = collectProductsFromEditor();
  }

  function renderProductEditors() {
    const list = document.getElementById("product-editor-list");
    list.innerHTML = "";
    if (!draft.products.length) {
      list.innerHTML = `<p class="editor-empty">${escapeHtml(ui.empty)}</p>`;
      return;
    }
    draft.products.forEach((product, index) => {
      const screenshot = imageSource(product);
      const item = document.createElement("details");
      item.className = "product-editor";
      item.dataset.productId = product.id;
      item.innerHTML = `
        <summary>
          <span class="project-index">${String(index + 1).padStart(2, "0")}</span>
          <span class="project-summary-name">${escapeHtml(product.name || ui.project)}</span>
          <span class="chevron">⌄</span>
        </summary>
        <div class="project-form">
          <div class="field-row two">
            <label>${escapeHtml(ui.name)}<input data-field="name" type="text" value="${escapeHtml(
              product.name || "",
            )}" maxlength="80"></label>
            <label>${escapeHtml(ui.status)}<input data-field="status" type="text" value="${escapeHtml(
              product.status || "",
            )}" maxlength="40"></label>
          </div>
          <label>${escapeHtml(ui.url)}<input data-field="url" type="url" value="${escapeHtml(
            product.url || "",
          )}" placeholder="https://example.com"></label>
          <div class="field-row two">
            <label>${escapeHtml(ui.category)}<input data-field="coverSub" type="text" value="${escapeHtml(
              product.coverSub || "",
            )}" maxlength="80"></label>
            <label>${escapeHtml(ui.tag)}<input data-field="tag" type="text" value="${escapeHtml(
              product.tag || "",
            )}" maxlength="120"></label>
          </div>
          <label>${escapeHtml(ui.features)}
            <textarea data-field="features" rows="4">${escapeHtml(
              (product.features || []).join("\n"),
            )}</textarea>
            <small>${escapeHtml(ui.featuresHint)}</small>
          </label>
          <label>${escapeHtml(ui.benefit)}
            <textarea data-field="benefit" rows="3">${escapeHtml(
              product.benefit || "",
            )}</textarea>
          </label>
          <div class="image-field">
            <div class="image-preview">${
              screenshot
                ? `<img src="${escapeHtml(screenshot)}" alt="">`
                : `<span>${escapeHtml(ui.screenshot)}</span>`
            }</div>
            <div>
              <b>${escapeHtml(ui.screenshot)}</b>
              <small>JPG, PNG. Изображение будет сжато и сохранено локально.</small>
              <label class="upload-button">${escapeHtml(
                screenshot ? ui.replaceImage : ui.upload,
              )}<input type="file" accept="image/png,image/jpeg,image/webp" data-image-upload hidden></label>
            </div>
          </div>
          <button class="delete-project" type="button" data-delete-project>${escapeHtml(
            ui.delete,
          )}</button>
        </div>`;
      list.appendChild(item);
    });
  }

  function addProduct() {
    refreshDraftFromForms();
    const id = `project-${Date.now()}-${Math.random()
      .toString(36)
      .slice(2, 7)}`;
    draft.products.push({
      id,
      name: "Новый проект",
      url: "",
      shot: "",
      coverSub: "",
      status: "Live",
      tag: "",
      features: [],
      benefit: "",
      badgeColor: ["r", "m", "f"][draft.products.length % 3],
      imageData: "",
    });
    renderProductEditors();
    const added = document.querySelector(
      `.product-editor[data-product-id="${CSS.escape(id)}"]`,
    );
    if (added) {
      added.open = true;
      added.scrollIntoView({ behavior: "smooth", block: "nearest" });
      added.querySelector('[data-field="name"]')?.focus();
    }
  }

  function deleteProduct(id) {
    if (!window.confirm(ui.deleteConfirm)) return;
    refreshDraftFromForms();
    draft.products = draft.products.filter((product) => product.id !== id);
    draftImages.delete(id);
    renderProductEditors();
  }

  async function compressImage(file) {
    if (!file.type.startsWith("image/")) {
      throw new Error("Not an image");
    }
    if (file.size > 18 * 1024 * 1024) {
      throw new Error("Image is too large");
    }
    const source = await loadImageFile(file);
    const maxWidth = 1440;
    const maxHeight = 1000;
    const scale = Math.min(1, maxWidth / source.width, maxHeight / source.height);
    const canvas = document.createElement("canvas");
    canvas.width = Math.max(1, Math.round(source.width * scale));
    canvas.height = Math.max(1, Math.round(source.height * scale));
    const context = canvas.getContext("2d");
    context.fillStyle = "#ffffff";
    context.fillRect(0, 0, canvas.width, canvas.height);
    context.drawImage(source, 0, 0, canvas.width, canvas.height);
    return canvas.toDataURL("image/jpeg", 0.82);
  }

  function loadImageFile(file) {
    return new Promise((resolve, reject) => {
      const image = new Image();
      const url = URL.createObjectURL(file);
      image.onload = () => {
        URL.revokeObjectURL(url);
        resolve(image);
      };
      image.onerror = () => {
        URL.revokeObjectURL(url);
        reject(new Error("Could not read image"));
      };
      image.src = url;
    });
  }

  function saveEditor() {
    refreshDraftFromForms();
    const nextProfile = clone(draft);
    try {
      persistProfile(nextProfile);
    } catch (error) {
      window.alert(ui.storageError);
      console.error(error);
      return;
    }
    renderProfile(nextProfile);
    closeEditor();
    showToast(ui.saved);
  }

  function resetProfile() {
    if (!window.confirm(ui.resetConfirm)) return;
    delete store.brand;
    delete store.contacts;
    if (store.languages) delete store.languages[profile.lang];
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(store));
    } catch {
      localStorage.removeItem(STORAGE_KEY);
      store = {};
    }
    profile = mergeProfile(baseConfig, store);
    draft = clone(profile);
    renderProductEditors();
    fillIdentityFields();
    renderProfile(profile);
    closeEditor();
  }

  function exportJson() {
    refreshDraftFromForms();
    const data = JSON.stringify(
      {
        version: 1,
        lang: profile.lang,
        brand: draft.brand,
        contacts: draft.contacts,
        products: draft.products,
      },
      null,
      2,
    );
    downloadBlob(
      new Blob([data], { type: "application/json" }),
      `profile-${profile.lang}.json`,
    );
  }

  async function readPublishedProfile() {
    if (window.location.protocol === "file:") return {};
    try {
      const response = await fetch(`profile-${baseConfig.lang}.json`, {
        cache: "no-store",
      });
      if (!response.ok) return {};
      const data = await response.json();
      return data && typeof data === "object" ? data : {};
    } catch {
      return {};
    }
  }

  async function importJson(file) {
    try {
      const parsed = JSON.parse(await file.text());
      if (!parsed || typeof parsed !== "object" || !Array.isArray(parsed.products)) {
        throw new Error("Invalid profile JSON");
      }
      refreshDraftFromForms();
      draft.brand = String(parsed.brand || draft.brand);
      draft.contacts = {
        ...draft.contacts,
        ...(parsed.contacts || {}),
      };
      draft.products = parsed.products.map((product, index) => ({
        ...product,
        id: String(product.id || `imported-${Date.now()}-${index}`),
        name: String(product.name || "Project"),
        url: String(product.url || ""),
        shot: String(product.shot || ""),
        coverSub: String(product.coverSub || ""),
        status: String(product.status || "Live"),
        tag: String(product.tag || ""),
        features: Array.isArray(product.features)
          ? product.features.map(String)
          : [],
        benefit: String(product.benefit || ""),
        badgeColor: ["r", "m", "f"].includes(product.badgeColor)
          ? product.badgeColor
          : "r",
        imageData: "",
      }));
      renderProductEditors();
      fillIdentityFields();
      showToast(ui.imported);
    } catch (error) {
      console.error(error);
      window.alert(ui.importError);
    }
  }

  function downloadBlob(blob, filename) {
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 2000);
  }

  function showToast(message) {
    let toast = document.getElementById("profile-toast");
    if (!toast) {
      toast = document.createElement("div");
      toast.id = "profile-toast";
      toast.className = "profile-toast";
      toast.setAttribute("role", "status");
      document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.classList.add("visible");
    clearTimeout(showToast.timer);
    showToast.timer = setTimeout(() => toast.classList.remove("visible"), 3200);
  }

  async function downloadWord() {
    const button = document.getElementById("download-word");
    const original = button.innerHTML;
    button.disabled = true;
    button.textContent = "Word…";
    try {
      if (!window.docx) throw new Error("Word builder is unavailable");
      const blob = await buildWordDocument(profile);
      downloadBlob(
        blob,
        `Company_Profile_${profile.lang.toUpperCase()}.docx`,
      );
    } catch (error) {
      console.error(error);
      window.alert("Не удалось сформировать Word. Обновите страницу и попробуйте ещё раз.");
    } finally {
      button.disabled = false;
      button.innerHTML = original;
    }
  }

  async function buildWordDocument(data) {
    const d = window.docx;
    const {
      Document,
      Packer,
      Paragraph,
      TextRun,
      HeadingLevel,
      AlignmentType,
      PageBreak,
      ExternalHyperlink,
      Table,
      TableRow,
      TableCell,
      WidthType,
      BorderStyle,
      ShadingType,
      VerticalAlign,
      ImageRun,
    } = d;

    const text = data.text;
    const brand = data.brand?.trim() || data.descriptor;
    const black = "000000";
    const navy = "17324D";
    const slate = "425466";
    const muted = "6B7C8F";
    const light = "EEF3F8";
    const border = "D9E2EC";
    const accent = "2F6FED";
    const pageWidth = 9360;
    const cellMargins = {
      top: 150,
      bottom: 150,
      left: 170,
      right: 170,
    };
    const emptyPortfolio =
      text.word_empty_portfolio ||
      "Add your first project through the website editor.";
    const emptyContacts =
      text.word_empty_contacts ||
      "Add your contact details through the website editor.";

    const paragraph = (value, options = {}) =>
      new Paragraph({
        spacing: { after: 120, line: 290, ...(options.spacing || {}) },
        ...options,
        children: options.runs || [
          new TextRun({
            text: String(value ?? ""),
            font: "Aptos",
            size: options.size || 21,
            color: options.color || "263746",
            bold: Boolean(options.bold),
            italics: Boolean(options.italics),
          }),
        ],
      });

    const label = (value) =>
      new Paragraph({
        spacing: { before: 80, after: 100 },
        children: [
          new TextRun({
            text: String(value).toUpperCase(),
            font: "Aptos",
            size: 17,
            bold: true,
            color: accent,
            characterSpacing: 18,
          }),
        ],
      });

    const heading = (value, level = 1) =>
      new Paragraph({
        heading: level === 1 ? HeadingLevel.HEADING_1 : HeadingLevel.HEADING_2,
        spacing:
          level === 1
            ? { before: 0, after: 220 }
            : { before: 260, after: 100 },
        keepNext: true,
        children: [
          new TextRun({
            text: String(value ?? ""),
            font: "Aptos Display",
            color: black,
            bold: true,
            size: level === 1 ? 34 : 26,
          }),
        ],
      });

    const bullet = (value) =>
      new Paragraph({
        text: String(value ?? ""),
        bullet: { level: 0 },
        spacing: { after: 70, line: 280 },
        style: "ProfileBullet",
      });

    const divider = () =>
      new Paragraph({
        spacing: { after: 1 },
        border: {
          bottom: {
            color: border,
            size: 6,
            style: BorderStyle.SINGLE,
            space: 1,
          },
        },
      });

    const pageBreak = () =>
      new Paragraph({
        spacing: { after: 0 },
        children: [new PageBreak()],
      });

    const contactLine = (labelText, value) => {
      if (!value) return null;
      return new Paragraph({
        spacing: { after: 90, line: 270 },
        children: [
          new TextRun({
            text: `${labelText}: `,
            font: "Aptos",
            size: 20,
            bold: true,
            color: navy,
          }),
          new TextRun({
            text: String(value),
            font: "Aptos",
            size: 20,
            color: slate,
          }),
        ],
      });
    };

    const hyperlinkParagraph = (value) => {
      const url = normalizeUrl(value);
      if (!url) return null;
      return new Paragraph({
        spacing: { after: 100 },
        children: [
          new ExternalHyperlink({
            link: url,
            children: [
              new TextRun({
                text: host(url),
                font: "Aptos",
                size: 19,
                color: accent,
                underline: {},
              }),
            ],
          }),
        ],
      });
    };

    const children = [
      label(`${data.docLabel} · ${data.year}`),
      new Paragraph({
        style: "ProfileTitle",
        spacing: { before: 260, after: 160 },
        children: [
          new TextRun({
            text: brand,
            font: "Aptos Display",
            size: 48,
            bold: true,
            color: black,
          }),
        ],
      }),
      ...(data.descriptor && data.descriptor !== brand
        ? [
            paragraph(data.descriptor, {
              size: 24,
              color: navy,
              bold: true,
              spacing: { after: 260 },
            }),
          ]
        : []),
      divider(),
      paragraph(text.cover_lead, {
        size: 25,
        color: slate,
        spacing: { before: 260, after: 260, line: 330 },
      }),
      paragraph(text.cover_sub, {
        size: 18,
        color: muted,
        bold: true,
        spacing: { after: 300 },
      }),
      label(text.cover_products_label),
      ...data.products.slice(0, 6).map((product) =>
        new Paragraph({
          spacing: { after: 70 },
          children: [
            new TextRun({
              text: "•  ",
              font: "Aptos",
              size: 21,
              color: accent,
              bold: true,
            }),
            new TextRun({
              text: product.name || "Project",
              font: "Aptos",
              size: 21,
              color: slate,
              bold: true,
            }),
            new TextRun({
              text: product.coverSub ? `  ${product.coverSub}` : "",
              font: "Aptos",
              size: 20,
              color: muted,
            }),
          ],
        }),
      ),
      pageBreak(),
      heading(`${text.p2_title_a} ${text.p2_title_b}`),
      paragraph(text.p2_lead, {
        size: 22,
        color: slate,
        spacing: { after: 240, line: 310 },
      }),
      label(text.p2_problems_label),
    ];

    for (const [title, body] of text.p2_problems) {
      children.push(heading(title, 2));
      children.push(
        paragraph(body, {
          size: 20,
          color: slate,
          spacing: { after: 120 },
        }),
      );
    }

    children.push(
      heading(text.p3_title),
      paragraph(text.p3_lead, {
        size: 21,
        color: slate,
        spacing: { after: 180 },
      }),
    );

    for (let i = 0; i < data.products.length; i += 1) {
      const product = data.products[i];
      children.push(heading(product.name || `Project ${i + 1}`, 2));
      if (product.tag) {
        children.push(
          paragraph(product.tag, {
            size: 21,
            color: navy,
            bold: true,
            spacing: { after: 80 },
          }),
        );
      }
      const link = hyperlinkParagraph(product.url);
      if (link) children.push(link);
      for (const feature of product.features || []) {
        if (String(feature).trim()) children.push(bullet(feature));
      }
      if (product.benefit) {
        children.push(
          paragraph(product.benefit, {
            size: 20,
            color: slate,
            spacing: { before: 120, after: 220, line: 290 },
            runs: [
              new TextRun({
                text: `${text.benefit_label || "Business value"}: `,
                font: "Aptos",
                size: 20,
                bold: true,
                color: accent,
              }),
              new TextRun({
                text: product.benefit,
                font: "Aptos",
                size: 20,
                color: slate,
              }),
            ],
          }),
        );
      }
    }

    if (!data.products.length) {
      children.push(
        paragraph(emptyPortfolio, {
          color: muted,
          italics: true,
        }),
      );
    }

    children.push(
      heading(text.p4_title),
      paragraph(text.p4_lead, {
        size: 21,
        color: slate,
        spacing: { after: 200 },
      }),
    );

    for (const [, title, body, example] of text.services) {
      children.push(heading(title, 2));
      children.push(
        paragraph(body, {
          size: 20,
          color: slate,
          spacing: { after: 80 },
        }),
      );
      children.push(
        paragraph(`${text.example_label}: ${example}`, {
          size: 18,
          color: muted,
          spacing: { after: 130 },
        }),
      );
    }

    children.push(
      pageBreak(),
      heading(`${text.p5_title_a} ${text.p5_title_b}`),
      paragraph(text.p5_lead, {
        size: 21,
        color: slate,
        spacing: { after: 180 },
      }),
      label(text.p5_phases_label),
    );
    for (const [phase, title, body] of text.p5_phases) {
      children.push(
        paragraph(`${phase} · ${title}`, {
          bold: true,
          color: navy,
          spacing: { after: 30 },
        }),
        paragraph(body, {
          color: slate,
          spacing: { after: 110 },
        }),
      );
    }
    for (const [, title, body] of text.benefits) {
      children.push(heading(title, 2));
      children.push(
        paragraph(body, {
          color: slate,
          spacing: { after: 120 },
        }),
      );
    }

    children.push(
      pageBreak(),
      heading(text.p6_title),
      label(text.models_label),
    );
    for (const [title, body] of text.models) {
      children.push(
        paragraph(title, {
          bold: true,
          color: navy,
          spacing: { after: 30 },
        }),
        paragraph(body, {
          color: slate,
          spacing: { after: 110 },
        }),
      );
    }
    children.push(
      label("Process"),
    );
    text.steps.forEach(([title, body], index) => {
      children.push(
        paragraph(`${index + 1}. ${title}`, {
          bold: true,
          color: navy,
          spacing: { before: 40, after: 20 },
          keepNext: true,
        }),
        paragraph(body, {
          color: slate,
          spacing: { after: 75 },
        }),
      );
    });
    children.push(
      paragraph(text.cta_a, {
        size: 23,
        bold: true,
        color: navy,
        spacing: { before: 180, after: 80 },
      }),
      paragraph(text.cta_b, {
        size: 23,
        bold: true,
        color: accent,
        spacing: { after: 140 },
      }),
      paragraph(text.cta_note, {
        color: slate,
        spacing: { after: 220 },
      }),
      label(
        text.word_contacts_label ||
          text.contact_labels?.website ||
          "Contacts",
      ),
    );

    const contactNodes = [
      contactLine("WhatsApp", data.contacts?.whatsapp),
      contactLine("Telegram", data.contacts?.telegram),
      contactLine("Email", data.contacts?.email),
      contactLine("Website", data.contacts?.website),
    ].filter(Boolean);
    if (contactNodes.length) {
      children.push(...contactNodes);
    } else {
      children.push(
        paragraph(emptyContacts, {
          color: muted,
          italics: true,
        }),
      );
    }

    const doc = new Document({
      creator: brand,
      title: `${data.docLabel} — ${brand}`,
      description: text.cover_lead,
      styles: {
        default: {
          document: {
            run: {
              font: "Aptos",
              size: 21,
              color: "263746",
            },
            paragraph: {
              spacing: { after: 120, line: 290 },
            },
          },
        },
        paragraphStyles: [
          {
            id: "ProfileTitle",
            name: "Profile Title",
            basedOn: "Title",
            next: "Normal",
            quickFormat: true,
            run: {
              font: "Aptos Display",
              size: 48,
              bold: true,
              color: black,
            },
            paragraph: {
              spacing: { before: 0, after: 160 },
            },
          },
          {
            id: "ProfileHeading1",
            name: "Profile Heading 1",
            basedOn: "Heading 1",
            next: "Normal",
            run: {
              font: "Aptos Display",
              size: 34,
              bold: true,
              color: black,
            },
            paragraph: {
              spacing: { before: 0, after: 220 },
              keepNext: true,
            },
          },
          {
            id: "ProfileHeading2",
            name: "Profile Heading 2",
            basedOn: "Heading 2",
            next: "Normal",
            run: {
              font: "Aptos Display",
              size: 26,
              bold: true,
              color: black,
            },
            paragraph: {
              spacing: { before: 260, after: 100 },
              keepNext: true,
            },
          },
          {
            id: "ProfileBullet",
            name: "Profile Bullet",
            basedOn: "List Bullet",
            next: "ProfileBullet",
            run: {
              font: "Aptos",
              size: 20,
              color: "263746",
            },
            paragraph: {
              spacing: { after: 70, line: 280 },
            },
          },
        ],
      },
      sections: [
        {
          properties: {
            titlePage: true,
            page: {
              size: {
                width: 11906,
                height: 16838,
              },
              margin: {
                top: 1080,
                right: 1150,
                bottom: 1080,
                left: 1150,
                header: 500,
                footer: 500,
              },
            },
          },
          children,
        },
      ],
    });

    return Packer.toBlob(doc);
  }

  function buildEditor() {
    const root = document.createElement("div");
    root.id = "profile-editor";
    root.className = "editor-shell";
    root.hidden = true;
    root.innerHTML = `
      <div class="editor-scrim" data-close-editor></div>
      <aside class="editor-panel" role="dialog" aria-modal="true" aria-labelledby="editor-title" tabindex="-1">
        <header class="editor-header">
          <div>
            <span class="editor-kicker">Company profile</span>
            <h2 id="editor-title">${escapeHtml(ui.title)}</h2>
            <p>${escapeHtml(ui.intro)}</p>
          </div>
          <button class="editor-close" type="button" data-close-editor aria-label="Закрыть">×</button>
        </header>
        <div class="editor-scroll">
          <section class="editor-section">
            <div class="section-heading">
              <span>01</span>
              <div><h3>${escapeHtml(ui.identity)}</h3><p>${escapeHtml(ui.brandHint)}</p></div>
            </div>
            <label>${escapeHtml(ui.brand)}<input id="editor-brand" type="text" maxlength="80" placeholder="Independent Software Studio"></label>
            <fieldset>
              <legend>${escapeHtml(ui.contacts)}</legend>
              <div class="field-row two">
                <label>${escapeHtml(ui.whatsapp)}<input id="editor-whatsapp" type="text" inputmode="tel" placeholder="+62 812 3456 7890"></label>
                <label>${escapeHtml(ui.telegram)}<input id="editor-telegram" type="text" placeholder="@username"></label>
              </div>
              <div class="field-row two">
                <label>${escapeHtml(ui.email)}<input id="editor-email" type="email" placeholder="name@company.com"></label>
                <label>${escapeHtml(ui.website)}<input id="editor-website" type="text" placeholder="your-domain.com"></label>
              </div>
            </fieldset>
          </section>
          <section class="editor-section">
            <div class="section-heading">
              <span>02</span>
              <div><h3>${escapeHtml(ui.portfolio)}</h3><p>${escapeHtml(ui.portfolioHint)}</p></div>
            </div>
            <div id="product-editor-list" class="product-editor-list"></div>
            <button class="add-project" id="add-project" type="button">+ ${escapeHtml(ui.addProject)}</button>
          </section>
          <section class="editor-section backup-section">
            <div class="section-heading">
              <span>03</span>
              <div><h3>${escapeHtml(ui.backup)}</h3><p>Данные хранятся в этом браузере. JSON-файл помогает перенести тексты на другое устройство.</p></div>
            </div>
            <div class="backup-actions">
              <button id="export-json" type="button">${escapeHtml(ui.exportJson)}</button>
              <button id="import-json" type="button">${escapeHtml(ui.importJson)}</button>
              <input id="import-json-file" type="file" accept="application/json,.json" hidden>
            </div>
            <button class="reset-profile" id="reset-profile" type="button">${escapeHtml(ui.reset)}</button>
          </section>
        </div>
        <footer class="editor-footer">
          <button class="editor-cancel" type="button" data-close-editor>${escapeHtml(ui.cancel)}</button>
          <button class="editor-save" id="save-profile" type="button">${escapeHtml(ui.save)}</button>
        </footer>
      </aside>`;
    document.body.appendChild(root);
  }

  function bindEvents() {
    document.getElementById("edit-profile")?.addEventListener("click", () => {
      if (serverMode) {
        window.location.href = "/admin";
      } else {
        openEditor();
      }
    });
    document
      .querySelectorAll("[data-close-editor]")
      .forEach((node) => node.addEventListener("click", closeEditor));
    document.getElementById("save-profile")?.addEventListener("click", saveEditor);
    document.getElementById("add-project")?.addEventListener("click", addProduct);
    document
      .getElementById("reset-profile")
      ?.addEventListener("click", resetProfile);
    document.getElementById("export-json")?.addEventListener("click", exportJson);
    document.getElementById("import-json")?.addEventListener("click", () => {
      document.getElementById("import-json-file").click();
    });
    document
      .getElementById("import-json-file")
      ?.addEventListener("change", async (event) => {
        const file = event.target.files?.[0];
        if (file) await importJson(file);
        event.target.value = "";
      });
    document
      .getElementById("download-pdf")
      ?.addEventListener("click", () => window.print());
    document
      .getElementById("download-word")
      ?.addEventListener("click", downloadWord);

    document
      .getElementById("product-editor-list")
      ?.addEventListener("input", (event) => {
        const editor = event.target.closest(".product-editor");
        if (!editor) return;
        if (event.target.dataset.field === "name") {
          editor.querySelector(".project-summary-name").textContent =
            event.target.value || ui.project;
        }
      });
    document
      .getElementById("product-editor-list")
      ?.addEventListener("change", async (event) => {
        if (!event.target.matches("[data-image-upload]")) return;
        const editor = event.target.closest(".product-editor");
        const file = event.target.files?.[0];
        if (!editor || !file) return;
        try {
          const imageData = await compressImage(file);
          const id = editor.dataset.productId;
          draftImages.set(id, imageData);
          editor.querySelector(".image-preview").innerHTML =
            `<img src="${escapeHtml(imageData)}" alt="">`;
          const upload = editor.querySelector(".upload-button");
          if (upload) upload.childNodes[0].textContent = ui.replaceImage;
        } catch (error) {
          console.error(error);
          window.alert("Не удалось обработать изображение. Используйте JPG или PNG.");
        }
      });
    document
      .getElementById("product-editor-list")
      ?.addEventListener("click", (event) => {
        const button = event.target.closest("[data-delete-project]");
        if (!button) return;
        const editor = button.closest(".product-editor");
        if (editor) deleteProduct(editor.dataset.productId);
      });

    window.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && editorOpen) closeEditor();
      if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "s" && editorOpen) {
        event.preventDefault();
        saveEditor();
      }
    });
    window.addEventListener("resize", rescaleDeck);
  }

  function initLanguageChooser() {
    const gate = document.getElementById("language-gate");
    const select = document.getElementById("language-select");
    if (!gate || !select) return;
    const stored = localStorage.getItem(LANGUAGE_KEY);

    select.addEventListener("change", () => {
      const option = select.options[select.selectedIndex];
      localStorage.setItem(LANGUAGE_KEY, option?.dataset.code || baseConfig.lang);
      window.location.href = select.value;
    });

    gate.querySelectorAll("[data-language-choice]").forEach((choice) => {
      choice.addEventListener("click", (event) => {
        event.preventDefault();
        localStorage.setItem(LANGUAGE_KEY, choice.dataset.languageChoice);
        const target = choice.getAttribute("href");
        if (choice.dataset.languageChoice === baseConfig.lang) {
          gate.hidden = true;
        } else {
          window.location.href = target;
        }
      });
    });

    if (!stored) {
      gate.hidden = false;
      document.body.classList.add("language-gate-open");
      gate
        .querySelector(`[data-language-choice="${baseConfig.lang}"]`)
        ?.classList.add("current");
    }
  }

  async function init() {
    buildEditor();
    bindEvents();
    const published = await readPublishedProfile();
    profile = mergeProfile(baseConfig, store, published);
    renderProfile(profile);
    initLanguageChooser();
    window.profileEditor = {
      open: openEditor,
      save: saveEditor,
      downloadWord,
      getProfile: () => clone(profile),
    };
  }

  init();
})();
