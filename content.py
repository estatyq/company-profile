# -*- coding: utf-8 -*-
"""All presentation copy and projects configuration.

To customize:
1. Set BRAND_NAME (or leave empty to show 'Independent Software Studio').
2. Fill in CONTACTS (WhatsApp, Telegram, Email, Website).
3. To ADD, REMOVE, or EDIT projects: just edit the PRODUCTS list below!
   Drop your screenshot in assets/screens/ (or assets/web/) and reference it in 'shot'.
4. Run:
   python build.py
   This will automatically update both PDFs and the website in site/ !
"""

# ==============================================================================
# 1. BRAND & CONTACTS
# ==============================================================================

import pathlib

LANGUAGES = {
    "en": {
        "label": "EN",
        "native": "English",
        "html": "index.html",
        "file_suffix": "EN",
    },
    "id": {
        "label": "ID",
        "native": "Bahasa Indonesia",
        "html": "id.html",
        "file_suffix": "ID",
    },
    "uk": {
        "label": "UA",
        "native": "Українська",
        "html": "uk.html",
        "file_suffix": "UK",
    },
    "de": {
        "label": "DE",
        "native": "Deutsch",
        "html": "de.html",
        "file_suffix": "DE",
    },
    "es": {
        "label": "ES",
        "native": "Español",
        "html": "es.html",
        "file_suffix": "ES",
    },
}

DEFAULT_LANGUAGE = "en"

# Name of your studio / personal brand.
BRAND_NAME = "xcombine"

# Contact info. Empty values are displayed as neat placeholders in the presentation.
CONTACTS = {
    "whatsapp": "",
    "telegram": "",
    "email": "help@xcombine.xyz",
    "website": "https://xcombine.xyz",
}

# Automatically load private local contacts from 'мои_контакты.txt' if present
for _p in [
    pathlib.Path(__file__).resolve().parent.parent / "мои_контакты.txt",
    pathlib.Path(__file__).resolve().parent / "мои_контакты.txt",
]:
    if _p.exists():
        try:
            for _line in _p.read_text(encoding="utf-8").splitlines():
                _line = _line.strip()
                if not _line or _line.startswith("#") or "=" not in _line:
                    continue
                _k, _v = _line.split("=", 1)
                _k = _k.strip().upper()
                _v = _v.strip()
                if _k in ("НАЗВАНИЕ_СТУДИИ", "BRAND_NAME", "NAME") and _v:
                    BRAND_NAME = _v
                elif _k in ("WHATSAPP", "WA", "PHONE") and _v:
                    CONTACTS["whatsapp"] = _v
                elif _k in ("TELEGRAM", "TG") and _v:
                    CONTACTS["telegram"] = _v
                elif _k in ("EMAIL", "MAIL", "ПОЧТА") and _v:
                    CONTACTS["email"] = _v
                elif _k in ("САЙТ", "WEBSITE", "SITE") and _v:
                    CONTACTS["website"] = _v
        except Exception:
            pass
        break

# ==============================================================================
# 2. PROJECTS PORTFOLIO (Add as many projects as you want!)
# ==============================================================================

PRODUCTS = [
    {
        "id": "rieltix",
        "name": "Rieltix",
        "url": "https://rieltix.com/",
        "shot": "rieltix_crm.jpg",      # image from assets/web/
        "badge_color": "r",             # 'r', 'm', 'f' or custom color
        "status": {
            "en": "Live", "id": "Aktif", "uk": "Активний",
            "de": "Live", "es": "Activo",
        },
        "cover_sub": {
            "en": "Real estate CRM", "id": "CRM properti",
            "uk": "CRM для нерухомості", "de": "CRM für Immobilien",
            "es": "CRM inmobiliario",
        },
        "tag": {
            "en": "CRM for real estate agencies",
            "id": "CRM untuk agen properti",
            "uk": "CRM для агентств нерухомості",
            "de": "CRM für Immobilienmakler",
            "es": "CRM para agencias inmobiliarias",
        },
        "features": {
            "en": [
                "Property and client database",
                "Team tasks and calendar",
                "Agency website with catalog and map",
                "Telegram integration, workflow automation",
            ],
            "id": [
                "Database properti dan klien",
                "Tugas tim dan kalender",
                "Website agen dengan katalog dan peta",
                "Integrasi Telegram dan otomatisasi",
            ],
            "uk": [
                "База об’єктів і клієнтів",
                "Завдання команди й календар",
                "Сайт агентства з каталогом і картою",
                "Інтеграція з Telegram та автоматизація",
            ],
            "de": [
                "Immobilien- und Kundendatenbank",
                "Teamaufgaben und Kalender",
                "Makler-Website mit Katalog und Karte",
                "Telegram-Integration und Automatisierung",
            ],
            "es": [
                "Base de propiedades y clientes",
                "Tareas del equipo y calendario",
                "Web de la agencia con catálogo y mapa",
                "Integración con Telegram y automatización",
            ],
        },
        "benefit": {
            "en": "Agents see the next step for every client — nothing gets lost between chats and spreadsheets.",
            "id": "Agen selalu tahu langkah berikutnya untuk setiap klien — tidak ada yang terlewat di antara chat dan spreadsheet.",
            "uk": "Агенти завжди бачать наступний крок для кожного клієнта — нічого не губиться між чатами й таблицями.",
            "de": "Makler sehen für jeden Kunden den nächsten Schritt — nichts geht zwischen Chats und Tabellen verloren.",
            "es": "Los agentes ven el siguiente paso para cada cliente: nada se pierde entre chats y hojas de cálculo.",
        },
    },
    {
        "id": "mapest",
        "name": "Mapest",
        "url": "https://mapest.app/",
        "shot": "mapest_platform.jpg",
        "badge_color": "m",
        "status": {
            "en": "Live", "id": "Aktif", "uk": "Активний",
            "de": "Live", "es": "Activo",
        },
        "cover_sub": {
            "en": "Property platform", "id": "Platform properti",
            "uk": "Платформа нерухомості", "de": "Immobilienplattform",
            "es": "Plataforma inmobiliaria",
        },
        "tag": {
            "en": "Property search & listings platform",
            "id": "Platform pencarian dan iklan properti",
            "uk": "Платформа пошуку та оголошень нерухомості",
            "de": "Such- und Immobilienportal",
            "es": "Plataforma de búsqueda y anuncios inmobiliarios",
        },
        "features": {
            "en": [
                "Listing aggregation and de-duplication",
                "Interactive map with area selection",
                "Structured catalog with detailed filters",
                "Automatic data updates, Telegram alerts",
            ],
            "id": [
                "Listing digabung, tanpa duplikat",
                "Peta interaktif dengan pilihan area",
                "Katalog terstruktur dengan filter lengkap",
                "Data diperbarui otomatis, notifikasi Telegram",
            ],
            "uk": [
                "Об’єднані оголошення без дублікатів",
                "Інтерактивна карта з вибором району",
                "Структурований каталог із детальними фільтрами",
                "Автоматичне оновлення даних і сповіщення в Telegram",
            ],
            "de": [
                "Zusammengeführte Angebote ohne Duplikate",
                "Interaktive Karte mit Gebietsauswahl",
                "Strukturierter Katalog mit detaillierten Filtern",
                "Automatische Datenupdates und Telegram-Hinweise",
            ],
            "es": [
                "Anuncios unificados sin duplicados",
                "Mapa interactivo con selección de zonas",
                "Catálogo estructurado con filtros detallados",
                "Actualización automática de datos y avisos por Telegram",
            ],
        },
        "benefit": {
            "en": "Large volumes of scattered data are collected, organized and kept up to date automatically.",
            "id": "Data dalam jumlah besar dari berbagai sumber dikumpulkan, dirapikan, dan diperbarui secara otomatis.",
            "uk": "Великі обсяги розрізнених даних збираються, упорядковуються та автоматично підтримуються в актуальному стані.",
            "de": "Große Mengen verstreuter Daten werden gesammelt, geordnet und automatisch aktuell gehalten.",
            "es": "Grandes volúmenes de datos dispersos se recopilan, ordenan y mantienen actualizados automáticamente.",
        },
    },
    {
        "id": "forma",
        "name": "Forma",
        "url": "https://forma.ink/",
        "shot": "forma_doc.jpg",
        "badge_color": "f",
        "status": {
            "en": "Live", "id": "Aktif", "uk": "Активний",
            "de": "Live", "es": "Activo",
        },
        "cover_sub": {
            "en": "AI documents", "id": "Dokumen berbasis AI",
            "uk": "Документи зі ШІ", "de": "Dokumente mit KI",
            "es": "Documentos con IA",
        },
        "tag": {
            "en": "Smart document builder with AI",
            "id": "Pembuat dokumen pintar berbasis AI",
            "uk": "Розумний конструктор документів зі ШІ",
            "de": "Intelligenter Dokumenteneditor mit KI",
            "es": "Creador inteligente de documentos con IA",
        },
        "features": {
            "en": [
                "Templates for letters, agreements, statements",
                "Live editor with instant preview",
                "AI help to improve and translate text",
                "Digital signature, export to PDF and Word",
            ],
            "id": [
                "Template surat, perjanjian, dan pernyataan",
                "Editor langsung dengan pratinjau instan",
                "AI untuk memperbaiki dan menerjemahkan",
                "Tanda tangan digital, ekspor PDF dan Word",
            ],
            "uk": [
                "Шаблони листів, договорів і заяв",
                "Редактор із миттєвим попереднім переглядом",
                "ШІ для покращення тексту й перекладу",
                "Електронний підпис, експорт у PDF і Word",
            ],
            "de": [
                "Vorlagen für Briefe, Verträge und Erklärungen",
                "Editor mit sofortiger Vorschau",
                "KI zum Verbessern und Übersetzen von Texten",
                "Digitale Signatur, Export nach PDF und Word",
            ],
            "es": [
                "Plantillas para cartas, contratos y declaraciones",
                "Editor con vista previa instantánea",
                "IA para mejorar y traducir textos",
                "Firma digital y exportación a PDF y Word",
            ],
        },
        "benefit": {
            "en": "Less time on routine paperwork — and documents that look consistent every time.",
            "id": "Lebih sedikit waktu untuk urusan administrasi — dokumen selalu tampil rapi dan seragam.",
            "uk": "Менше часу на рутинні документи — і завжди однакове охайне оформлення.",
            "de": "Weniger Zeit für Routinepapierkram — und jedes Dokument sieht einheitlich und professionell aus.",
            "es": "Menos tiempo en trámites rutinarios y documentos siempre ordenados y coherentes.",
        },
    },
]

# Quick lookup map
PRODUCT_URLS = {p["id"]: p["url"] for p in PRODUCTS}


# ==============================================================================
# 3. TEXTS & TRANSLATIONS (EN & ID)
# ==============================================================================

T = {
    # ------------------------------------------------------------------ ENGLISH
    "en": {
        "lang": "en",
        "descriptor": "Independent Software Studio",
        "brand_submark": "software product studio",
        "doc_label": "Company Profile",
        "year": "2026",
        # Page 1 — cover
        "cover_chip": "Software Product Studio",
        "cover_eyebrow": "Software · AI · Automation",
        "cover_title_a": "Your business has a problem.",
        "cover_title_b": "We build the solution.",
        "cover_sub": "Products / Engineering / Automation",
        "cover_lead": "Explore ready-to-use software, order a custom solution, or help shape a new product built around your industry's needs.",
        "cover_cta_primary": "Discuss your idea",
        "cover_cta_secondary": "Explore products",
        "cover_trust": "Built for real operations. Designed to evolve.",
        "cover_products_label": "Ready-to-use products",
        # Page 2 — who we are / problem
        "p2_eyebrow": "01 — How we solve it",
        "p2_title_a": "One problem.",
        "p2_title_b": "Multiple ways to solve it.",
        "p2_lead": "We start with the business need, then choose the right delivery model instead of forcing every client into custom development.",
        "p2_problems_label": "Three ways to work",
        "p2_problems": [
            ("Custom development", "A unique system built for your processes, integrations and operating model."),
            ("Ready-to-use products", "Choose an existing product with subscription or licensing, plus optional setup and adaptation."),
            ("Product partnership", "A recurring problem becomes a shared product built and evolved with its first clients."),
        ],
        "p2_flow_label": "From problem to product",
        "p2_flow": [
            ("Describe the need", "what should work better"),
            ("Validate the fit", "custom or reusable"),
            ("Choose the model", "scope, ownership, pricing"),
            ("Launch", "build, integrate, onboard"),
            ("Evolve", "feedback improves the product"),
        ],
        "p2_cmp_label": "A clear commercial boundary",
        "p2_cmp_head": ("Custom project", "Product subscription"),
        "p2_cmp": [
            ("One client with unique requirements", "Many clients with shared functionality"),
            ("Paid development and implementation", "A recurring access fee"),
            ("Client-specific features stay separate", "Shared features make the product stronger"),
        ],
        # Page 3 — products
        "p3_eyebrow": "02 — Our products",
        "p3_title": "Real products built for real operations.",
        "p3_title_continued": "More products built for real business needs.",
        "p3_lead": "Each one started from a practical business problem. The same experience goes into every custom project.",
        "benefit_label": "What it delivers",
        # Page 4 — services
        "p4_eyebrow": "03 — Custom development",
        "p4_title": "Software built around your operation",
        "p4_lead": "When ready-made tools do not fit, we design the system, integrations and automation around your actual process.",
        "example_label": "For example",
        "services": [
            ("crm", "CRM & Business Management", "All clients, deals and tasks in one place. You can see what is happening in your business at any moment.", "Sales pipeline, team tasks, owner dashboard"),
            ("bot", "AI Assistants & Chatbots", "Answer common questions 24/7, collect client details and pass ready requests to your team.", "WhatsApp / Telegram bots, website chat. Voice AI assistant — in development"),
            ("zap", "Business Process Automation", "Repetitive tasks run on their own: reminders, notifications, reports and data transfer.", "Automatic follow-ups, daily reports, document generation"),
            ("globe", "Websites & Web Applications", "A fast, modern website that sends client requests straight into your system.", "Company website, product catalog, client portal"),
            ("code", "Custom Software Development", "Software built for your exact process when ready-made tools don’t fit.", "Internal systems, booking, inventory, price calculators"),
            ("link", "API & System Integrations", "Your tools talk to each other — no more copying data by hand between apps.", "CRM + messengers + payments + spreadsheets"),
        ],
        # Page 5 — why us
        "p5_eyebrow": "04 — Product partnership",
        "p5_title_a": "Start with a client problem.",
        "p5_title_b": "Build a product others need.",
        "p5_lead": "When the same need appears across companies, we validate a shared product and evolve it with early users.",
        "p5_phases_label": "Three stages",
        "p5_phases": [
            ("Stage 1", "Validate", "Test recurring demand and the economics"),
            ("Stage 2", "Launch", "Define ownership, pricing and scope"),
            ("Stage 3", "Scale", "Feedback drives the shared product"),
        ],
        "benefits": [
            ("target", "Recurring problem", "We look for a need shared by several companies, not a one-off request."),
            ("sliders", "Commercial validation", "Demand, willingness to pay and support costs are tested before scaling."),
            ("check", "Clear ownership", "Code, data and product rights are defined before development starts."),
            ("wallet", "Defined subscription", "The service scope and pricing are attached to the shared product."),
            ("layers", "Shared roadmap", "Common features evolve for all users; unique needs remain extensions."),
            ("refresh", "Continuous evolution", "Client feedback becomes a structured input into product development."),
        ],
        # Page 6 — cooperation & contacts
        "p6_eyebrow": "05 — Start a conversation",
        "p6_title": "How we work",
        "steps": [
            ("Discuss the task", "A short conversation about your business and goals."),
            ("Analyze needs", "We map the process and decide what to automate first."),
            ("Solution & cost", "A clear proposal: scope, timeline and price."),
            ("Build & test", "Regular demos, so you always see the progress."),
            ("Launch & grow", "Go live, onboard the team, keep improving."),
        ],
        "models_label": "Two ways to start",
        "models": [
            ("Custom project", "A defined build for your own operation."),
            ("Product partnership", "Start with a shared problem and explore a reusable product."),
        ],
        "cta_a": "Have a business problem others may share?",
        "cta_b": "Let’s explore whether it should become a product.",
        "cta_note": "Tell us about the process, who feels the pain and what success should look like.",
        "contact_labels": {"whatsapp": "WhatsApp", "telegram": "Telegram", "email": "Email", "website": "Website"},
        "contact_placeholders": {"whatsapp": "your WhatsApp number", "telegram": "@username", "email": "name@company.com", "website": "your-website.com"},
        "ui_download_pdf": "Download PDF",
        "ui_whatsapp_chat": "Chat on WhatsApp",
        "ui_edit": "Edit",
        "ui_more_projects": "More projects",
        "ui_view_portfolio": "View portfolio",
        "ui_open_product": "Open product",
        "ui_view_project": "View project",
        "ui_manage_content": "Manage content",
        "nav_products": "Products",
        "nav_development": "Development",
        "nav_partnership": "Partnership",
        "nav_process": "How we work",
        "nav_contact": "Contact",
        "export_title": "Company presentation",
        "export_note": "Download the current multilingual PDF or editable Word document.",
        "word_empty_portfolio": "Add your first project through the website editor.",
        "word_empty_contacts": "Add your contact details through the website editor.",
        "word_contacts_label": "Contacts",
    },
    # --------------------------------------------------------------- INDONESIAN
    "id": {
        "lang": "id",
        "descriptor": "Independent Software Studio",
        "brand_submark": "studio produk software",
        "doc_label": "Profil Perusahaan",
        "year": "2026",
        # Page 1
        "cover_chip": "Studio Produk Software",
        "cover_eyebrow": "Software · AI · Otomatisasi",
        "cover_title_a": "Ada masalah bisnis?",
        "cover_title_b": "Kami membangun solusinya.",
        "cover_sub": "Produk / Rekayasa / Otomatisasi",
        "cover_lead": "Jelajahi software siap pakai, pesan solusi khusus, atau bantu membentuk produk baru untuk kebutuhan industri Anda.",
        "cover_cta_primary": "Diskusikan kebutuhan Anda",
        "cover_cta_secondary": "Lihat produk",
        "cover_trust": "Dibuat untuk operasional nyata. Dirancang untuk terus berkembang.",
        "cover_products_label": "Produk siap pakai",
        # Page 2
        "p2_eyebrow": "01 — Cara kami menyelesaikan",
        "p2_title_a": "Satu masalah.",
        "p2_title_b": "Beberapa cara untuk menyelesaikannya.",
        "p2_lead": "Kami mulai dari kebutuhan bisnis, lalu memilih model pengerjaan yang tepat — bukan memaksa setiap klien memakai pengembangan khusus.",
        "p2_problems_label": "Tiga cara bekerja",
        "p2_problems": [
            ("Pengembangan khusus", "Sistem unik yang dibangun untuk proses, integrasi, dan model operasional Anda."),
            ("Produk siap pakai", "Pilih produk yang sudah tersedia dengan langganan atau lisensi, beserta opsi implementasi dan penyesuaian."),
            ("Kemitraan produk", "Masalah yang berulang menjadi produk bersama yang dibangun dan dikembangkan bersama klien pertama."),
        ],
        "p2_flow_label": "Dari masalah menjadi produk",
        "p2_flow": [
            ("Jelaskan kebutuhan", "apa yang harus bekerja lebih baik"),
            ("Validasi kesesuaian", "khusus atau dapat digunakan ulang"),
            ("Pilih model", "lingkup, kepemilikan, harga"),
            ("Luncurkan", "bangun, integrasikan, terapkan"),
            ("Kembangkan", "masukan pengguna memperbaiki produk"),
        ],
        "p2_cmp_label": "Batas komersial yang jelas",
        "p2_cmp_head": ("Proyek khusus", "Langganan produk"),
        "p2_cmp": [
            ("Satu klien dengan kebutuhan unik", "Banyak klien dengan fungsi bersama"),
            ("Membayar pengembangan dan implementasi", "Biaya akses berulang"),
            ("Fitur khusus klien tetap terpisah", "Fitur bersama memperkuat produk"),
        ],
        # Page 3
        "p3_eyebrow": "02 — Produk kami",
        "p3_title": "Produk nyata untuk operasional nyata.",
        "p3_title_continued": "Produk lain untuk kebutuhan bisnis nyata.",
        "p3_lead": "Setiap produk berawal dari masalah bisnis yang nyata. Pengalaman yang sama kami bawa ke setiap proyek.",
        "benefit_label": "Hasil yang diberikan",
        # Page 4
        "p4_eyebrow": "03 — Pengembangan khusus",
        "p4_title": "Software yang dibangun untuk operasional Anda",
        "p4_lead": "Saat aplikasi siap pakai tidak cocok, kami merancang sistem, integrasi, dan otomatisasi sesuai proses nyata Anda.",
        "example_label": "Contoh",
        "services": [
            ("crm", "CRM & Manajemen Bisnis", "Semua klien, transaksi, dan tugas ada di satu tempat. Anda bisa memantau kondisi bisnis kapan saja.", "Alur penjualan, tugas tim, dasbor pemilik"),
            ("bot", "Asisten AI & Chatbot", "Menjawab pertanyaan umum 24 jam, mencatat data klien, lalu meneruskan permintaan yang sudah lengkap ke tim Anda.", "Bot WhatsApp / Telegram, chat di website. Asisten suara AI — sedang dikembangkan"),
            ("zap", "Otomatisasi Proses Bisnis", "Tugas berulang berjalan sendiri: pengingat, notifikasi, laporan, dan pemindahan data.", "Tindak lanjut otomatis, laporan harian, pembuatan dokumen"),
            ("globe", "Website & Aplikasi Web", "Website modern yang cepat dan langsung meneruskan permintaan klien ke sistem Anda.", "Website perusahaan, katalog produk, portal klien"),
            ("code", "Software Buatan Khusus", "Software yang dibuat sesuai proses Anda, saat aplikasi siap pakai tidak cocok.", "Sistem internal, pemesanan, stok barang, kalkulator harga"),
            ("link", "API & Integrasi Sistem", "Aplikasi-aplikasi Anda saling terhubung — tidak perlu lagi menyalin data secara manual.", "CRM + aplikasi chat + pembayaran + spreadsheet"),
        ],
        # Page 5
        "p5_eyebrow": "04 — Kemitraan produk",
        "p5_title_a": "Mulai dari masalah klien.",
        "p5_title_b": "Bangun produk yang dibutuhkan banyak orang.",
        "p5_lead": "Saat kebutuhan yang sama muncul di banyak perusahaan, kami memvalidasi produk bersama dan mengembangkannya bersama pengguna awal.",
        "p5_phases_label": "Tiga tahap",
        "p5_phases": [
            ("Tahap 1", "Validasi", "Uji kebutuhan berulang dan ekonominya"),
            ("Tahap 2", "Peluncuran", "Tetapkan kepemilikan, harga, dan lingkup"),
            ("Tahap 3", "Perluasan", "Masukan pengguna mengembangkan produk"),
        ],
        "benefits": [
            ("target", "Masalah berulang", "Kami mencari kebutuhan yang dialami beberapa perusahaan, bukan permintaan satu kali."),
            ("sliders", "Validasi komersial", "Permintaan, kesediaan membayar, dan biaya dukungan diuji sebelum produk diperluas."),
            ("check", "Kepemilikan jelas", "Hak atas kode, data, dan produk ditetapkan sebelum pengembangan dimulai."),
            ("wallet", "Langganan yang jelas", "Lingkup layanan dan harga terkait langsung dengan produk bersama."),
            ("layers", "Peta jalan bersama", "Fitur umum berkembang untuk semua pengguna; kebutuhan unik tetap menjadi ekstensi."),
            ("refresh", "Perkembangan berkelanjutan", "Masukan klien menjadi dasar pengembangan produk berikutnya."),
        ],
        # Page 6
        "p6_eyebrow": "05 — Mulai percakapan",
        "p6_title": "Cara kami bekerja",
        "steps": [
            ("Membahas kebutuhan", "Obrolan singkat tentang bisnis dan tujuan Anda."),
            ("Menganalisis kebutuhan", "Kami memetakan proses dan menentukan apa yang diotomatisasi lebih dulu."),
            ("Solusi & biaya", "Proposal yang jelas: cakupan, jadwal, dan harga."),
            ("Pembuatan & uji coba", "Demo berkala, sehingga Anda selalu bisa melihat perkembangannya."),
            ("Peluncuran & lanjutan", "Sistem mulai dipakai, tim dilatih, dan produk terus ditingkatkan."),
        ],
        "models_label": "Dua cara memulai",
        "models": [
            ("Proyek khusus", "Sistem tertentu untuk operasional Anda sendiri."),
            ("Kemitraan produk", "Mulai dari masalah bersama dan kembangkan produk yang dapat digunakan ulang."),
        ],
        "cta_a": "Punya masalah bisnis yang mungkin dialami perusahaan lain?",
        "cta_b": "Mari kita lihat apakah masalah itu layak menjadi produk.",
        "cta_note": "Ceritakan prosesnya, siapa yang merasakan masalahnya, dan seperti apa hasil yang diinginkan.",
        "contact_labels": {"whatsapp": "WhatsApp", "telegram": "Telegram", "email": "Email", "website": "Website"},
        "contact_placeholders": {"whatsapp": "nomor WhatsApp Anda", "telegram": "@username", "email": "nama@perusahaan.com", "website": "website-anda.com"},
        "ui_download_pdf": "Unduh PDF",
        "ui_whatsapp_chat": "Chat di WhatsApp",
        "ui_edit": "Kelola",
        "ui_more_projects": "Proyek lainnya",
        "ui_view_portfolio": "Lihat portofolio",
        "ui_open_product": "Buka produk",
        "ui_view_project": "Lihat proyek",
        "ui_manage_content": "Kelola konten",
        "nav_products": "Produk",
        "nav_development": "Pengembangan",
        "nav_partnership": "Kemitraan",
        "nav_process": "Cara kerja",
        "nav_contact": "Kontak",
        "export_title": "Presentasi perusahaan",
        "export_note": "Unduh PDF multibahasa terbaru atau dokumen Word yang dapat diedit.",
        "word_empty_portfolio": "Tambahkan proyek pertama melalui editor di website.",
        "word_empty_contacts": "Tambahkan kontak melalui editor di website.",
        "word_contacts_label": "Kontak",
    },
    # --------------------------------------------------------------- UKRAINIAN
    "uk": {
        "lang": "uk",
        "descriptor": "Незалежна студія програмного забезпечення",
        "brand_submark": "студія програмних продуктів",
        "doc_label": "Профіль компанії",
        "year": "2026",
        "cover_chip": "Студія програмних продуктів",
        "cover_eyebrow": "ПЗ · ШІ · Автоматизація",
        "cover_title_a": "Проблема у вашому бізнесі?",
        "cover_title_b": "Ми створюємо рішення.",
        "cover_sub": "Продукти / Розробка / Автоматизація",
        "cover_lead": "Обирайте готове програмне забезпечення, замовляйте індивідуальне рішення або допоможіть створити продукт для потреб вашої галузі.",
        "cover_cta_primary": "Обговорити ідею",
        "cover_cta_secondary": "Переглянути продукти",
        "cover_trust": "Створено для реальної роботи. Розраховано на розвиток.",
        "cover_products_label": "Готові продукти",
        "p2_eyebrow": "01 — Як ми вирішуємо",
        "p2_title_a": "Одна проблема.",
        "p2_title_b": "Кілька способів її вирішити.",
        "p2_lead": "Ми починаємо з бізнес-потреби, а вже потім обираємо модель роботи, не примушуючи кожного клієнта до індивідуальної розробки.",
        "p2_problems_label": "Три формати роботи",
        "p2_problems": [
            ("Індивідуальна розробка", "Унікальна система для ваших процесів, інтеграцій та операційної моделі."),
            ("Готові продукти", "Існуючий продукт за підпискою або ліцензією з можливим налаштуванням і впровадженням."),
            ("Партнерство над продуктом", "Повторювана проблема стає спільним продуктом, який розвивають разом із першими клієнтами."),
        ],
        "p2_flow_label": "Від проблеми до продукту",
        "p2_flow": [
            ("Опишіть потребу", "що має працювати краще"),
            ("Перевірте підхід", "індивідуальний чи повторюваний"),
            ("Оберіть модель", "обсяг, права, вартість"),
            ("Запустіть", "розробка, інтеграція, впровадження"),
            ("Розвивайте", "відгуки покращують продукт"),
        ],
        "p2_cmp_label": "Чітка комерційна межа",
        "p2_cmp_head": ("Індивідуальний проєкт", "Підписка на продукт"),
        "p2_cmp": [
            ("Один клієнт з унікальними вимогами", "Багато клієнтів зі спільними функціями"),
            ("Оплата розробки та впровадження", "Регулярна плата за доступ"),
            ("Специфічні функції залишаються окремими", "Спільні функції зміцнюють продукт"),
        ],
        "p3_eyebrow": "02 — Наші продукти",
        "p3_title": "Реальні продукти для реальної роботи.",
        "p3_title_continued": "Більше продуктів для реальних бізнес-потреб.",
        "p3_lead": "Кожен із них починався з практичної бізнес-проблеми. Цей самий досвід ми вкладаємо в кожен індивідуальний проєкт.",
        "benefit_label": "Що це дає",
        "p4_eyebrow": "03 — Індивідуальна розробка",
        "p4_title": "Програмне забезпечення під вашу роботу",
        "p4_lead": "Коли готові інструменти не підходять, ми створюємо систему, інтеграції та автоматизацію навколо вашого реального процесу.",
        "example_label": "Наприклад",
        "services": [
            ("crm", "CRM та управління бізнесом", "Усі клієнти, угоди й завдання в одному місці. Ви бачите, що відбувається в бізнесі в будь-який момент.", "Воронка продажів, завдання команди, панель власника"),
            ("bot", "ШІ-асистенти та чат-боти", "Відповідають на типові запитання 24/7, збирають дані клієнта й передають команді готовий запит.", "Боти WhatsApp / Telegram, чат на сайті. Голосовий ШІ-асистент — у розробці"),
            ("zap", "Автоматизація бізнес-процесів", "Повторювані дії виконуються самі: нагадування, сповіщення, звіти й перенесення даних.", "Автоматичні нагадування, щоденні звіти, створення документів"),
            ("globe", "Сайти та вебзастосунки", "Швидкий сучасний сайт, який передає запити клієнтів безпосередньо у вашу систему.", "Сайт компанії, каталог продуктів, клієнтський портал"),
            ("code", "Індивідуальна розробка ПЗ", "Програма, створена під ваш процес, коли готові рішення не підходять.", "Внутрішні системи, бронювання, облік, калькулятори цін"),
            ("link", "API та системні інтеграції", "Ваші інструменти обмінюються даними — більше жодного ручного копіювання.", "CRM + месенджери + платежі + таблиці"),
        ],
        "p5_eyebrow": "04 — Партнерство над продуктом",
        "p5_title_a": "Почніть із проблеми клієнта.",
        "p5_title_b": "Створіть продукт, потрібний іншим.",
        "p5_lead": "Коли однакова потреба виникає в різних компаніях, ми перевіряємо спільний продукт і розвиваємо його разом із першими користувачами.",
        "p5_phases_label": "Три етапи",
        "p5_phases": [
            ("Етап 1", "Перевірка", "Тестуємо повторюваний попит та економіку"),
            ("Етап 2", "Запуск", "Визначаємо права, ціну та обсяг"),
            ("Етап 3", "Масштабування", "Відгуки розвивають спільний продукт"),
        ],
        "benefits": [
            ("target", "Повторювана проблема", "Шукаємо потребу, спільну для кількох компаній, а не одноразовий запит."),
            ("sliders", "Комерційна перевірка", "До масштабування перевіряємо попит, готовність платити й витрати на підтримку."),
            ("check", "Чіткі права", "Права на код, дані та продукт визначаються до початку розробки."),
            ("wallet", "Визначена підписка", "Обсяг сервісу та ціна прив’язані до спільного продукту."),
            ("layers", "Спільна дорожня карта", "Загальні функції розвиваються для всіх, унікальні залишаються розширеннями."),
            ("refresh", "Постійний розвиток", "Відгуки клієнтів стають структурованим джерелом для розвитку продукту."),
        ],
        "p6_eyebrow": "05 — Почнімо розмову",
        "p6_title": "Як ми працюємо",
        "steps": [
            ("Обговорення задачі", "Коротка розмова про ваш бізнес і цілі."),
            ("Аналіз потреб", "Визначаємо процеси й те, що варто автоматизувати першим."),
            ("Рішення й вартість", "Чітка пропозиція: обсяг робіт, строки та ціна."),
            ("Розробка й тестування", "Регулярні демонстрації, щоб ви бачили прогрес."),
            ("Запуск і розвиток", "Запускаємо систему, навчаємо команду й продовжуємо вдосконалення."),
        ],
        "models_label": "Два способи старту",
        "models": [
            ("Індивідуальний проєкт", "Окрема система для вашої власної роботи."),
            ("Партнерство над продуктом", "Почніть зі спільної проблеми та дослідіть можливість повторно використовуваного продукту."),
        ],
        "cta_a": "Маєте бізнес-проблему, яку можуть мати й інші компанії?",
        "cta_b": "Перевірмо, чи варто перетворити її на продукт.",
        "cta_note": "Розкажіть про процес, хто відчуває проблему та яким має бути результат.",
        "contact_labels": {"whatsapp": "WhatsApp", "telegram": "Telegram", "email": "Email", "website": "Сайт"},
        "contact_placeholders": {"whatsapp": "ваш номер WhatsApp", "telegram": "@username", "email": "name@company.com", "website": "vash-sait.com"},
        "ui_download_pdf": "Завантажити PDF",
        "ui_whatsapp_chat": "Написати у WhatsApp",
        "ui_edit": "Редагувати",
        "ui_more_projects": "Ще проєкти",
        "ui_view_portfolio": "Переглянути портфоліо",
        "ui_open_product": "Відкрити продукт",
        "ui_view_project": "Переглянути проєкт",
        "ui_manage_content": "Керувати контентом",
        "nav_products": "Продукти",
        "nav_development": "Розробка",
        "nav_partnership": "Партнерство",
        "nav_process": "Як ми працюємо",
        "nav_contact": "Контакти",
        "export_title": "Презентація компанії",
        "export_note": "Завантажте актуальну PDF-версію або редагований документ Word.",
        "word_empty_portfolio": "Додайте перший проєкт через редактор на сайті.",
        "word_empty_contacts": "Додайте контакти через редактор на сайті.",
        "word_contacts_label": "Контакти",
    },
    # ------------------------------------------------------------------ GERMAN
    "de": {
        "lang": "de",
        "descriptor": "Unabhängiges Softwarestudio",
        "brand_submark": "software-produktstudio",
        "doc_label": "Unternehmensprofil",
        "year": "2026",
        "cover_chip": "Software-Produktstudio",
        "cover_eyebrow": "Software · KI · Automatisierung",
        "cover_title_a": "Ihr Unternehmen hat ein Problem.",
        "cover_title_b": "Wir entwickeln die Lösung.",
        "cover_sub": "Produkte / Engineering / Automatisierung",
        "cover_lead": "Nutzen Sie fertige Software, bestellen Sie eine individuelle Lösung oder gestalten Sie ein neues Produkt für die Anforderungen Ihrer Branche.",
        "cover_cta_primary": "Idee besprechen",
        "cover_cta_secondary": "Produkte entdecken",
        "cover_trust": "Für den realen Betrieb gebaut. Für Weiterentwicklung konzipiert.",
        "cover_products_label": "Sofort einsetzbare Produkte",
        "p2_eyebrow": "01 — Unser Lösungsweg",
        "p2_title_a": "Ein Problem.",
        "p2_title_b": "Mehrere Wege zur Lösung.",
        "p2_lead": "Wir beginnen mit dem Geschäftsbedarf und wählen dann das passende Modell, statt jeden Kunden in die Individualentwicklung zu zwingen.",
        "p2_problems_label": "Drei Arbeitsmodelle",
        "p2_problems": [
            ("Individuelle Entwicklung", "Ein einzigartiges System für Ihre Prozesse, Integrationen und Betriebsabläufe."),
            ("Fertige Produkte", "Ein bestehendes Produkt per Abo oder Lizenz, optional mit Einrichtung und Anpassung."),
            ("Produktpartnerschaft", "Ein wiederkehrendes Problem wird zum gemeinsamen Produkt mit den ersten Kunden."),
        ],
        "p2_flow_label": "Vom Problem zum Produkt",
        "p2_flow": [
            ("Bedarf beschreiben", "was besser funktionieren soll"),
            ("Eignung prüfen", "individuell oder wiederverwendbar"),
            ("Modell wählen", "Umfang, Rechte, Preis"),
            ("Starten", "entwickeln, integrieren, einführen"),
            ("Weiterentwickeln", "Feedback verbessert das Produkt"),
        ],
        "p2_cmp_label": "Eine klare kommerzielle Grenze",
        "p2_cmp_head": ("Individuelles Projekt", "Produktabo"),
        "p2_cmp": [
            ("Ein Kunde mit besonderen Anforderungen", "Viele Kunden mit gemeinsamen Funktionen"),
            ("Bezahlte Entwicklung und Einführung", "Wiederkehrende Zugangsgebühr"),
            ("Spezifische Funktionen bleiben getrennt", "Gemeinsame Funktionen stärken das Produkt"),
        ],
        "p3_eyebrow": "02 — Unsere Produkte",
        "p3_title": "Echte Produkte für den realen Betrieb.",
        "p3_title_continued": "Weitere Produkte für reale Geschäftsanforderungen.",
        "p3_lead": "Jedes Produkt entstand aus einem praktischen Geschäftsproblem. Diese Erfahrung fließt in jedes individuelle Projekt ein.",
        "benefit_label": "Was es leistet",
        "p4_eyebrow": "03 — Individuelle Entwicklung",
        "p4_title": "Software für Ihren tatsächlichen Betrieb",
        "p4_lead": "Wenn Standardwerkzeuge nicht passen, gestalten wir System, Integrationen und Automatisierung entlang Ihres realen Prozesses.",
        "example_label": "Zum Beispiel",
        "services": [
            ("crm", "CRM & Unternehmensführung", "Alle Kunden, Geschäfte und Aufgaben an einem Ort. Sie sehen jederzeit, was im Unternehmen passiert.", "Vertriebspipeline, Teamaufgaben, Inhaber-Dashboard"),
            ("bot", "KI-Assistenten & Chatbots", "Beantworten häufige Fragen rund um die Uhr, erfassen Kundendaten und übergeben fertige Anfragen an Ihr Team.", "WhatsApp- / Telegram-Bots, Website-Chat. KI-Sprachassistent — in Entwicklung"),
            ("zap", "Geschäftsprozess-Automatisierung", "Wiederkehrende Aufgaben laufen selbstständig: Erinnerungen, Benachrichtigungen, Berichte und Datenübertragung.", "Automatische Follow-ups, Tagesberichte, Dokumenterstellung"),
            ("globe", "Websites & Webanwendungen", "Eine schnelle, moderne Website, die Kundenanfragen direkt in Ihr System überträgt.", "Unternehmenswebsite, Produktkatalog, Kundenportal"),
            ("code", "Individuelle Softwareentwicklung", "Software für Ihre genauen Abläufe, wenn Standardlösungen nicht passen.", "Interne Systeme, Buchung, Lagerverwaltung, Preisrechner"),
            ("link", "API- & Systemintegrationen", "Ihre Anwendungen tauschen Daten aus — kein manuelles Kopieren mehr.", "CRM + Messenger + Zahlungen + Tabellen"),
        ],
        "p5_eyebrow": "04 — Produktpartnerschaft",
        "p5_title_a": "Beginnen Sie mit dem Problem eines Kunden.",
        "p5_title_b": "Bauen Sie ein Produkt, das auch andere brauchen.",
        "p5_lead": "Wenn derselbe Bedarf in mehreren Unternehmen auftritt, validieren wir ein gemeinsames Produkt und entwickeln es mit frühen Nutzern weiter.",
        "p5_phases_label": "Drei Phasen",
        "p5_phases": [
            ("Phase 1", "Validierung", "Wiederkehrenden Bedarf und Wirtschaftlichkeit prüfen"),
            ("Phase 2", "Start", "Eigentum, Preis und Leistungsumfang festlegen"),
            ("Phase 3", "Skalierung", "Feedback entwickelt das gemeinsame Produkt"),
        ],
        "benefits": [
            ("target", "Wiederkehrendes Problem", "Wir suchen einen Bedarf mehrerer Unternehmen, nicht nur eine einmalige Anfrage."),
            ("sliders", "Kommerzielle Validation", "Bedarf, Zahlungsbereitschaft und Supportkosten werden vor dem Ausbau geprüft."),
            ("check", "Klares Eigentum", "Rechte an Code, Daten und Produkt werden vor Entwicklungsstart festgelegt."),
            ("wallet", "Definiertes Abo", "Leistungsumfang und Preis werden direkt am gemeinsamen Produkt festgemacht."),
            ("layers", "Gemeinsame Roadmap", "Gemeinsame Funktionen entwickeln sich für alle; individuelle Bedürfnisse bleiben Erweiterungen."),
            ("refresh", "Kontinuierliche Entwicklung", "Kundenfeedback wird strukturiert in die Produktentwicklung eingebunden."),
        ],
        "p6_eyebrow": "05 — Ins Gespräch kommen",
        "p6_title": "So arbeiten wir",
        "steps": [
            ("Aufgabe besprechen", "Ein kurzes Gespräch über Ihr Unternehmen und Ihre Ziele."),
            ("Bedarf analysieren", "Wir erfassen die Prozesse und legen fest, was zuerst automatisiert wird."),
            ("Lösung & Kosten", "Ein klares Angebot: Umfang, Zeitplan und Preis."),
            ("Entwickeln & testen", "Regelmäßige Demos, damit Sie den Fortschritt immer sehen."),
            ("Starten & ausbauen", "Livegang, Team-Schulung und kontinuierliche Weiterentwicklung."),
        ],
        "models_label": "Zwei Startwege",
        "models": [
            ("Individuelles Projekt", "Eine definierte Lösung für Ihren eigenen Betrieb."),
            ("Produktpartnerschaft", "Beginnen Sie mit einem gemeinsamen Problem und prüfen Sie ein wiederverwendbares Produkt."),
        ],
        "cta_a": "Sie haben ein Geschäftsproblem, das auch andere Unternehmen haben könnten?",
        "cta_b": "Prüfen wir, ob daraus ein Produkt entstehen sollte.",
        "cta_note": "Beschreiben Sie den Prozess, wer betroffen ist und was das gewünschte Ergebnis ist.",
        "contact_labels": {"whatsapp": "WhatsApp", "telegram": "Telegram", "email": "E-Mail", "website": "Website"},
        "contact_placeholders": {"whatsapp": "Ihre WhatsApp-Nummer", "telegram": "@username", "email": "name@unternehmen.de", "website": "ihre-website.de"},
        "ui_download_pdf": "PDF herunterladen",
        "ui_whatsapp_chat": "WhatsApp-Chat",
        "ui_edit": "Bearbeiten",
        "ui_more_projects": "Weitere Projekte",
        "ui_view_portfolio": "Portfolio ansehen",
        "ui_open_product": "Produkt öffnen",
        "ui_view_project": "Projekt ansehen",
        "ui_manage_content": "Inhalte verwalten",
        "nav_products": "Produkte",
        "nav_development": "Entwicklung",
        "nav_partnership": "Partnerschaft",
        "nav_process": "Arbeitsweise",
        "nav_contact": "Kontakt",
        "export_title": "Unternehmenspräsentation",
        "export_note": "Laden Sie die aktuelle mehrsprachige PDF- oder bearbeitbare Word-Datei herunter.",
        "word_empty_portfolio": "Fügen Sie das erste Projekt über den Website-Editor hinzu.",
        "word_empty_contacts": "Fügen Sie Ihre Kontaktdaten über den Website-Editor hinzu.",
        "word_contacts_label": "Kontakt",
    },
    # ----------------------------------------------------------------- SPANISH
    "es": {
        "lang": "es",
        "descriptor": "Estudio independiente de software",
        "brand_submark": "estudio de productos software",
        "doc_label": "Perfil de la empresa",
        "year": "2026",
        "cover_chip": "Estudio de productos de software",
        "cover_eyebrow": "Software · IA · Automatización",
        "cover_title_a": "Tu negocio tiene un reto.",
        "cover_title_b": "Creamos la solución.",
        "cover_sub": "Productos / Ingeniería / Automatización",
        "cover_lead": "Explora software listo para usar, solicita una solución a medida o ayuda a crear un producto para las necesidades de tu sector.",
        "cover_cta_primary": "Hablemos de tu idea",
        "cover_cta_secondary": "Explorar productos",
        "cover_trust": "Diseñado para operaciones reales. Preparado para evolucionar.",
        "cover_products_label": "Productos listos para usar",
        "p2_eyebrow": "01 — Cómo resolvemos",
        "p2_title_a": "Un problema.",
        "p2_title_b": "Varias formas de resolverlo.",
        "p2_lead": "Empezamos por la necesidad del negocio y después elegimos el modelo adecuado, sin obligar a cada cliente a contratar desarrollo a medida.",
        "p2_problems_label": "Tres formas de trabajar",
        "p2_problems": [
            ("Desarrollo a medida", "Un sistema único para tus procesos, integraciones y modelo operativo."),
            ("Productos listos para usar", "Un producto existente por suscripción o licencia, con implantación y adaptación opcionales."),
            ("Colaboración de producto", "Un problema recurrente se convierte en un producto compartido que evoluciona con los primeros clientes."),
        ],
        "p2_flow_label": "Del problema al producto",
        "p2_flow": [
            ("Describe la necesidad", "qué debe funcionar mejor"),
            ("Valida el enfoque", "a medida o reutilizable"),
            ("Elige el modelo", "alcance, propiedad y precio"),
            ("Lanza", "desarrolla, integra y forma al equipo"),
            ("Evoluciona", "el feedback mejora el producto"),
        ],
        "p2_cmp_label": "Un límite comercial claro",
        "p2_cmp_head": ("Proyecto a medida", "Suscripción de producto"),
        "p2_cmp": [
            ("Un cliente con requisitos únicos", "Muchos clientes con funciones compartidas"),
            ("Pago por desarrollo e implantación", "Cuota periódica de acceso"),
            ("Las funciones específicas quedan separadas", "Las funciones compartidas fortalecen el producto"),
        ],
        "p3_eyebrow": "02 — Nuestros productos",
        "p3_title": "Productos reales para operaciones reales.",
        "p3_title_continued": "Más productos para necesidades reales de negocio.",
        "p3_lead": "Cada producto nació de un problema empresarial práctico. Aportamos esa misma experiencia a cada proyecto a medida.",
        "benefit_label": "Qué aporta",
        "p4_eyebrow": "03 — Desarrollo a medida",
        "p4_title": "Software construido alrededor de tu operación",
        "p4_lead": "Cuando las herramientas estándar no encajan, diseñamos el sistema, las integraciones y la automatización alrededor de tu proceso real.",
        "example_label": "Por ejemplo",
        "services": [
            ("crm", "CRM y gestión empresarial", "Todos los clientes, oportunidades y tareas en un solo lugar. Puedes ver qué ocurre en tu negocio en cualquier momento.", "Embudo de ventas, tareas del equipo, panel del propietario"),
            ("bot", "Asistentes de IA y chatbots", "Responden preguntas habituales 24/7, recopilan datos del cliente y envían solicitudes completas a tu equipo.", "Bots de WhatsApp / Telegram, chat web. Asistente de voz con IA — en desarrollo"),
            ("zap", "Automatización de procesos", "Las tareas repetitivas se ejecutan solas: recordatorios, avisos, informes y traslado de datos.", "Seguimientos automáticos, informes diarios, generación de documentos"),
            ("globe", "Websites y aplicaciones web", "Una web rápida y moderna que envía las solicitudes del cliente directamente a tu sistema.", "Web corporativa, catálogo de productos, portal de clientes"),
            ("code", "Desarrollo de software a medida", "Software creado para tus procesos exactos cuando las herramientas estándar no encajan.", "Sistemas internos, reservas, inventario, calculadoras de precios"),
            ("link", "API e integraciones", "Tus aplicaciones intercambian datos: no más copias manuales.", "CRM + mensajería + pagos + hojas de cálculo"),
        ],
        "p5_eyebrow": "04 — Colaboración de producto",
        "p5_title_a": "Empieza con el problema de un cliente.",
        "p5_title_b": "Crea un producto que otros necesiten.",
        "p5_lead": "Cuando la misma necesidad aparece en varias empresas, validamos un producto compartido y lo hacemos evolucionar con los primeros usuarios.",
        "p5_phases_label": "Tres etapas",
        "p5_phases": [
            ("Etapa 1", "Validar", "Probamos la demanda recurrente y su economía"),
            ("Etapa 2", "Lanzar", "Definimos propiedad, precio y alcance"),
            ("Etapa 3", "Escalar", "El feedback desarrolla el producto compartido"),
        ],
        "benefits": [
            ("target", "Problema recurrente", "Buscamos una necesidad compartida por varias empresas, no un encargo puntual."),
            ("sliders", "Validación comercial", "Probamos demanda, disposición a pagar y costes de soporte antes de escalar."),
            ("check", "Propiedad clara", "Los derechos sobre código, datos y producto se definen antes de desarrollar."),
            ("wallet", "Suscripción definida", "El alcance del servicio y el precio se vinculan al producto compartido."),
            ("layers", "Hoja de ruta común", "Las funciones comunes evolucionan para todos; las necesidades únicas quedan como extensiones."),
            ("refresh", "Evolución continua", "El feedback de los clientes se convierte en una fuente estructurada para el producto."),
        ],
        "p6_eyebrow": "05 — Iniciemos una conversación",
        "p6_title": "Cómo trabajamos",
        "steps": [
            ("Hablamos de la necesidad", "Una conversación breve sobre tu negocio y tus objetivos."),
            ("Analizamos los requisitos", "Mapeamos el proceso y decidimos qué automatizar primero."),
            ("Solución y coste", "Una propuesta clara: alcance, calendario y precio."),
            ("Desarrollo y pruebas", "Demos periódicas para que veas siempre el avance."),
            ("Lanzamiento y crecimiento", "Ponemos el sistema en marcha, formamos al equipo y seguimos mejorando."),
        ],
        "models_label": "Dos formas de empezar",
        "models": [
            ("Proyecto a medida", "Una solución definida para tu propia operación."),
            ("Colaboración de producto", "Empieza con un problema compartido y explora un producto reutilizable."),
        ],
        "cta_a": "¿Tienes un problema de negocio que otras empresas podrían compartir?",
        "cta_b": "Veamos si debería convertirse en un producto.",
        "cta_note": "Cuéntanos cómo funciona el proceso, quién sufre el problema y qué resultado buscas.",
        "contact_labels": {"whatsapp": "WhatsApp", "telegram": "Telegram", "email": "Correo", "website": "Web"},
        "contact_placeholders": {"whatsapp": "tu número de WhatsApp", "telegram": "@username", "email": "nombre@empresa.com", "website": "tu-web.com"},
        "ui_download_pdf": "Descargar PDF",
        "ui_whatsapp_chat": "Hablar por WhatsApp",
        "ui_edit": "Editar",
        "ui_more_projects": "Más proyectos",
        "ui_view_portfolio": "Ver portafolio",
        "ui_open_product": "Abrir producto",
        "ui_view_project": "Ver proyecto",
        "ui_manage_content": "Gestionar contenido",
        "nav_products": "Productos",
        "nav_development": "Desarrollo",
        "nav_partnership": "Colaboración",
        "nav_process": "Cómo trabajamos",
        "nav_contact": "Contacto",
        "export_title": "Presentación de la empresa",
        "export_note": "Descarga el PDF multilingüe actual o un documento Word editable.",
        "word_empty_portfolio": "Añade el primer proyecto desde el editor de la web.",
        "word_empty_contacts": "Añade los datos de contacto desde el editor de la web.",
        "word_contacts_label": "Contacto",
    },
}


def language_text(lang: str) -> dict:
    """Return complete copy with English fallbacks for a newly added language."""
    result = dict(T[DEFAULT_LANGUAGE])
    result.update(T.get(lang, {}))
    return result


def product_text(product: dict, key: str, lang: str):
    """Return localized product content with an English fallback."""
    value = product.get(key, "")
    if not isinstance(value, dict):
        return value
    return value.get(lang, value.get(DEFAULT_LANGUAGE, ""))

