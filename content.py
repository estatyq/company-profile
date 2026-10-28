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
    "email": "",
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
        "shot": "mapest_cards.jpg",
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
        "doc_label": "Company Profile",
        "year": "2026",
        # Page 1 — cover
        "cover_chip": "Company Profile · 2026",
        "cover_eyebrow": "Software · AI · Automation",
        "cover_title_a": "Digital solutions that",
        "cover_title_b": "work for your business",
        "cover_sub": "Software Development • AI Automation • Business Solutions",
        "cover_lead": "An independent developer of CRM systems, web platforms, AI assistants and business automation — built around how your company really works.",
        "cover_products_label": "Our live products",
        # Page 2 — who we are / problem
        "p2_eyebrow": "01 — Who we are",
        "p2_title_a": "Your business grows.",
        "p2_title_b": "Manual work shouldn’t grow with it.",
        "p2_lead": "We are an independent software developer. We build CRM systems, web platforms, AI assistants and automations — tailored to your business, not the other way around.",
        "p2_problems_label": "Where time gets lost",
        "p2_problems": [
            ("Data is scattered everywhere", "Clients in Excel, conversations in WhatsApp, tasks in someone’s head. Information gets lost between tools."),
            ("The same work, every day", "Answering identical questions, copying data, preparing documents and reports by hand."),
            ("Slow replies, missed leads", "When a request waits hours for an answer, the client may simply choose a competitor."),
        ],
        "p2_flow_label": "How it can work instead",
        "p2_flow": [
            ("New request", "website, WhatsApp, Telegram"),
            ("AI assistant", "replies and collects details"),
            ("Saved to CRM", "client card is created"),
            ("Task for the team", "with owner and deadline"),
            ("Auto reminder", "nothing is forgotten"),
        ],
        "p2_cmp_label": "Why custom instead of off-the-shelf?",
        "p2_cmp_head": ("Off-the-shelf software", "Custom solution"),
        "p2_cmp": [
            ("You pay for features you never use", "Only the features your business needs"),
            ("Your team adapts to the software", "The software follows your process"),
            ("Hard to connect with other tools", "Integrated with the services you already use"),
        ],
        # Page 3 — products
        "p3_eyebrow": "02 — Our products",
        "p3_title": "Real products — designed, built and launched by us.",
        "p3_title_continued": "More products built for real business needs.",
        "p3_lead": "Each one started from a practical business problem. The same experience goes into every custom project.",
        "benefit_label": "Business value",
        # Page 4 — services
        "p4_eyebrow": "03 — What we build",
        "p4_title": "What we can build for your business",
        "p4_lead": "We start from the result you need — and only then choose the technology.",
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
        "p5_eyebrow": "04 — Why work with us",
        "p5_title_a": "The right technology,",
        "p5_title_b": "with a personal approach.",
        "p5_lead": "You work directly with the developer who builds your product — no layers of managers in between.",
        "p5_phases_label": "Step-by-step rollout",
        "p5_phases": [
            ("Phase 1", "Core", "One key process is automated"),
            ("Phase 2", "Integrations", "Connect the tools you already use"),
            ("Phase 3", "AI & scale", "Assistants, analytics, new features"),
        ],
        "benefits": [
            ("target", "Built around you", "No templates forced on your team. We study your process and build exactly what it needs."),
            ("sliders", "Flexible and direct", "You talk to the developer directly. Decisions are fast, changes are easy to discuss."),
            ("check", "Proven by real products", "Rieltix, Mapest and Forma are online — you can see the quality before we start."),
            ("wallet", "Sensible budget", "Only the features you need, without big-agency overhead. Pay per project or monthly."),
            ("layers", "Gradual implementation", "Start with one important process, see the result, then expand step by step."),
            ("refresh", "Support and growth", "After launch we maintain and improve the product on agreed terms."),
        ],
        # Page 6 — cooperation & contacts
        "p6_eyebrow": "05 — Let’s work together",
        "p6_title": "How we work",
        "steps": [
            ("Discuss the task", "A short conversation about your business and goals."),
            ("Analyze needs", "We map the process and decide what to automate first."),
            ("Solution & cost", "A clear proposal: scope, timeline and price."),
            ("Build & test", "Regular demos, so you always see the progress."),
            ("Launch & grow", "Go live, onboard the team, keep improving."),
        ],
        "models_label": "Ways to cooperate",
        "models": [
            ("Custom project", "A solution built from scratch for your specific task."),
            ("Monthly subscription", "Selected services and products are available on a monthly plan."),
        ],
        "cta_a": "Have an idea or a business problem you want to automate?",
        "cta_b": "Let’s discuss the solution.",
        "cta_note": "Write to us — we’ll reply and arrange a convenient time for a consultation.",
        "contact_labels": {"whatsapp": "WhatsApp", "telegram": "Telegram", "email": "Email", "website": "Website"},
        "contact_placeholders": {"whatsapp": "your WhatsApp number", "telegram": "@username", "email": "name@company.com", "website": "your-website.com"},
        "ui_download_pdf": "Download PDF",
        "ui_whatsapp_chat": "Chat on WhatsApp",
        "ui_edit": "Edit",
        "ui_more_projects": "More projects",
        "ui_view_portfolio": "View portfolio",
        "word_empty_portfolio": "Add your first project through the website editor.",
        "word_empty_contacts": "Add your contact details through the website editor.",
        "word_contacts_label": "Contacts",
    },
    # --------------------------------------------------------------- INDONESIAN
    "id": {
        "lang": "id",
        "descriptor": "Independent Software Studio",
        "doc_label": "Profil Perusahaan",
        "year": "2026",
        # Page 1
        "cover_chip": "Profil Perusahaan · 2026",
        "cover_eyebrow": "Software · AI · Otomatisasi",
        "cover_title_a": "Solusi digital yang",
        "cover_title_b": "bekerja untuk bisnis Anda",
        "cover_sub": "Pengembangan Software • Otomatisasi AI • Solusi Bisnis",
        "cover_lead": "Pengembang independen yang membuat sistem CRM, platform web, asisten AI, dan otomatisasi bisnis — dirancang mengikuti cara kerja perusahaan Anda.",
        "cover_products_label": "Produk kami yang sudah berjalan",
        # Page 2
        "p2_eyebrow": "01 — Tentang kami",
        "p2_title_a": "Bisnis Anda terus berkembang.",
        "p2_title_b": "Pekerjaan manual jangan ikut membesar.",
        "p2_lead": "Kami pengembang software independen. Kami membuat sistem CRM, platform web, asisten AI, dan otomatisasi yang disesuaikan dengan bisnis Anda — bukan sebaliknya.",
        "p2_problems_label": "Di mana waktu terbuang",
        "p2_problems": [
            ("Data tersebar di banyak tempat", "Data klien di Excel, percakapan di WhatsApp, tugas hanya diingat-ingat. Informasi mudah tercecer."),
            ("Pekerjaan sama, setiap hari", "Menjawab pertanyaan yang itu-itu saja, menyalin data, serta menyusun dokumen dan laporan secara manual."),
            ("Balasan lambat, calon klien hilang", "Jika permintaan baru dibalas berjam-jam kemudian, calon klien bisa langsung memilih pesaing."),
        ],
        "p2_flow_label": "Sebagai gantinya, alurnya bisa begini",
        "p2_flow": [
            ("Pesan masuk", "website, WhatsApp, Telegram"),
            ("Asisten AI", "membalas dan mencatat data"),
            ("Tersimpan di CRM", "kartu klien dibuat otomatis"),
            ("Tugas untuk tim", "lengkap dengan penanggung jawab dan tenggat"),
            ("Pengingat otomatis", "tidak ada yang terlewat"),
        ],
        "p2_cmp_label": "Mengapa harus solusi khusus?",
        "p2_cmp_head": ("Software siap pakai", "Solusi khusus"),
        "p2_cmp": [
            ("Membayar fitur yang tidak pernah dipakai", "Hanya fitur yang dibutuhkan bisnis Anda"),
            ("Tim harus menyesuaikan diri dengan software", "Software mengikuti proses kerja Anda"),
            ("Sulit terhubung dengan aplikasi lain", "Terhubung dengan layanan yang sudah Anda pakai"),
        ],
        # Page 3
        "p3_eyebrow": "02 — Produk kami",
        "p3_title": "Produk nyata — kami rancang, bangun, dan luncurkan sendiri.",
        "p3_title_continued": "Produk lain untuk kebutuhan bisnis nyata.",
        "p3_lead": "Setiap produk berawal dari masalah bisnis yang nyata. Pengalaman yang sama kami bawa ke setiap proyek.",
        "benefit_label": "Manfaat bisnis",
        # Page 4
        "p4_eyebrow": "03 — Layanan",
        "p4_title": "Apa yang bisa kami bangun untuk bisnis Anda",
        "p4_lead": "Kami mulai dari hasil yang Anda inginkan — baru setelah itu memilih teknologinya.",
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
        "p5_eyebrow": "04 — Mengapa kami",
        "p5_title_a": "Teknologi yang tepat,",
        "p5_title_b": "dengan pendekatan personal.",
        "p5_lead": "Anda bekerja langsung dengan pengembang yang membuat produk Anda — tanpa lapisan manajer di tengah.",
        "p5_phases_label": "Pelaksanaan bertahap",
        "p5_phases": [
            ("Tahap 1", "Inti", "Satu proses utama diotomatisasi"),
            ("Tahap 2", "Integrasi", "Menghubungkan aplikasi yang sudah Anda pakai"),
            ("Tahap 3", "AI & perluasan", "Asisten AI, analisis data, fitur baru"),
        ],
        "benefits": [
            ("target", "Dibuat khusus untuk Anda", "Tanpa template yang dipaksakan. Kami mempelajari proses Anda, lalu membangun tepat sesuai kebutuhannya."),
            ("sliders", "Langsung dan fleksibel", "Anda berbicara langsung dengan pengembangnya. Keputusan cepat, perubahan mudah dibahas."),
            ("check", "Terbukti lewat produk nyata", "Rieltix, Mapest, dan Forma sudah berjalan — Anda bisa melihat kualitasnya sebelum memulai."),
            ("wallet", "Anggaran yang wajar", "Hanya fitur yang Anda perlukan, tanpa biaya tambahan seperti di agensi besar. Bisa per proyek atau bulanan."),
            ("layers", "Penerapan bertahap", "Mulai dari satu proses penting, lihat hasilnya, lalu kembangkan selangkah demi selangkah."),
            ("refresh", "Dukungan & pengembangan", "Setelah peluncuran, kami merawat dan menyempurnakan produk sesuai ketentuan yang disepakati."),
        ],
        # Page 6
        "p6_eyebrow": "05 — Mari bekerja sama",
        "p6_title": "Cara kami bekerja",
        "steps": [
            ("Membahas kebutuhan", "Obrolan singkat tentang bisnis dan tujuan Anda."),
            ("Menganalisis kebutuhan", "Kami memetakan proses dan menentukan apa yang diotomatisasi lebih dulu."),
            ("Solusi & biaya", "Proposal yang jelas: cakupan, jadwal, dan harga."),
            ("Pembuatan & uji coba", "Demo berkala, sehingga Anda selalu bisa melihat perkembangannya."),
            ("Peluncuran & lanjutan", "Sistem mulai dipakai, tim dilatih, dan produk terus ditingkatkan."),
        ],
        "models_label": "Pilihan kerja sama",
        "models": [
            ("Proyek khusus", "Solusi yang dibangun dari nol untuk kebutuhan spesifik Anda."),
            ("Langganan bulanan", "Layanan dan produk tertentu tersedia dengan biaya bulanan."),
        ],
        "cta_a": "Punya ide atau masalah bisnis yang ingin diotomatisasi?",
        "cta_b": "Mari kita bahas solusinya.",
        "cta_note": "Kirim pesan kepada kami — kami akan membalas dan mengatur jadwal konsultasi yang nyaman.",
        "contact_labels": {"whatsapp": "WhatsApp", "telegram": "Telegram", "email": "Email", "website": "Website"},
        "contact_placeholders": {"whatsapp": "nomor WhatsApp Anda", "telegram": "@username", "email": "nama@perusahaan.com", "website": "website-anda.com"},
        "ui_download_pdf": "Unduh PDF",
        "ui_whatsapp_chat": "Chat di WhatsApp",
        "ui_edit": "Kelola",
        "ui_more_projects": "Proyek lainnya",
        "ui_view_portfolio": "Lihat portofolio",
        "word_empty_portfolio": "Tambahkan proyek pertama melalui editor di website.",
        "word_empty_contacts": "Tambahkan kontak melalui editor di website.",
        "word_contacts_label": "Kontak",
    },
    # --------------------------------------------------------------- UKRAINIAN
    "uk": {
        "lang": "uk",
        "descriptor": "Незалежна студія програмного забезпечення",
        "doc_label": "Профіль компанії",
        "year": "2026",
        "cover_chip": "Профіль компанії · 2026",
        "cover_eyebrow": "ПЗ · ШІ · Автоматизація",
        "cover_title_a": "Цифрові рішення, що",
        "cover_title_b": "працюють для вашого бізнесу",
        "cover_sub": "Розробка ПЗ • Автоматизація зі ШІ • Бізнес-рішення",
        "cover_lead": "Незалежний розробник систем CRM, вебплатформ, ШІ-асистентів і бізнес-автоматизації — з урахуванням того, як насправді працює ваша компанія.",
        "cover_products_label": "Наші продукти, що вже працюють",
        "p2_eyebrow": "01 — Про нас",
        "p2_title_a": "Ваш бізнес зростає.",
        "p2_title_b": "Ручна робота не повинна зростати разом із ним.",
        "p2_lead": "Ми — незалежна студія розробки програмного забезпечення. Створюємо CRM, вебплатформи, ШІ-асистентів та автоматизації, адаптовані до ваших процесів, а не навпаки.",
        "p2_problems_label": "Де втрачається час",
        "p2_problems": [
            ("Дані розкидані по різних місцях", "Клієнти в Excel, розмови в WhatsApp, завдання лише в голові. Інформація губиться між інструментами."),
            ("Та сама робота щодня", "Повторні відповіді, копіювання даних, ручне створення документів і звітів."),
            ("Повільні відповіді, втрачені клієнти", "Якщо відповіді доводиться чекати годинами, потенційний клієнт може обрати конкурента."),
        ],
        "p2_flow_label": "Як це може працювати натомість",
        "p2_flow": [
            ("Новий запит", "сайт, WhatsApp, Telegram"),
            ("ШІ-асистент", "відповідає та збирає дані"),
            ("Збережено в CRM", "картка клієнта створюється автоматично"),
            ("Завдання для команди", "з відповідальним і дедлайном"),
            ("Автонагадування", "нічого не забуто"),
        ],
        "p2_cmp_label": "Чому індивідуальне рішення?",
        "p2_cmp_head": ("Готове програмне забезпечення", "Індивідуальне рішення"),
        "p2_cmp": [
            ("Ви платите за функції, які не використовуєте", "Лише функції, потрібні вашому бізнесу"),
            ("Команда підлаштовується під програму", "Програма працює за вашими процесами"),
            ("Складно інтегрувати з іншими сервісами", "Інтеграція з інструментами, які ви вже використовуєте"),
        ],
        "p3_eyebrow": "02 — Наші продукти",
        "p3_title": "Реальні продукти, які ми спроєктували, створили й запустили.",
        "p3_title_continued": "Більше продуктів для реальних бізнес-потреб.",
        "p3_lead": "Кожен із них починався з практичної бізнес-проблеми. Цей самий досвід ми вкладаємо в кожен індивідуальний проєкт.",
        "benefit_label": "Цінність для бізнесу",
        "p4_eyebrow": "03 — Що ми створюємо",
        "p4_title": "Що ми можемо створити для вашого бізнесу",
        "p4_lead": "Ми починаємо з потрібного вам результату й лише потім обираємо технології.",
        "example_label": "Наприклад",
        "services": [
            ("crm", "CRM та управління бізнесом", "Усі клієнти, угоди й завдання в одному місці. Ви бачите, що відбувається в бізнесі в будь-який момент.", "Воронка продажів, завдання команди, панель власника"),
            ("bot", "ШІ-асистенти та чат-боти", "Відповідають на типові запитання 24/7, збирають дані клієнта й передають команді готовий запит.", "Боти WhatsApp / Telegram, чат на сайті. Голосовий ШІ-асистент — у розробці"),
            ("zap", "Автоматизація бізнес-процесів", "Повторювані дії виконуються самі: нагадування, сповіщення, звіти й перенесення даних.", "Автоматичні нагадування, щоденні звіти, створення документів"),
            ("globe", "Сайти та вебзастосунки", "Швидкий сучасний сайт, який передає запити клієнтів безпосередньо у вашу систему.", "Сайт компанії, каталог продуктів, клієнтський портал"),
            ("code", "Індивідуальна розробка ПЗ", "Програма, створена під ваш процес, коли готові рішення не підходять.", "Внутрішні системи, бронювання, облік, калькулятори цін"),
            ("link", "API та системні інтеграції", "Ваші інструменти обмінюються даними — більше жодного ручного копіювання.", "CRM + месенджери + платежі + таблиці"),
        ],
        "p5_eyebrow": "04 — Чому ми",
        "p5_title_a": "Правильні технології",
        "p5_title_b": "з персональним підходом.",
        "p5_lead": "Ви працюєте безпосередньо з розробником, який створює ваш продукт, без прошарку менеджерів.",
        "p5_phases_label": "Поетапне впровадження",
        "p5_phases": [
            ("Етап 1", "Основа", "Автоматизовано один ключовий процес"),
            ("Етап 2", "Інтеграції", "Підключення інструментів, які ви вже використовуєте"),
            ("Етап 3", "ШІ та масштабування", "Асистенти, аналітика, нові функції"),
        ],
        "benefits": [
            ("target", "Створено для вас", "Жодних нав’язаних шаблонів. Ми вивчаємо процеси й створюємо саме те, що потрібно."),
            ("sliders", "Пряма й гнучка робота", "Ви спілкуєтеся з розробником напряму. Рішення ухвалюються швидко, зміни легко обговорити."),
            ("check", "Перевірено реальними продуктами", "Rieltix, Mapest і Forma працюють — якість можна оцінити ще до початку співпраці."),
            ("wallet", "Розумний бюджет", "Лише потрібні функції без накладних витрат великої агенції. Оплата за проєкт або щомісяця."),
            ("layers", "Поступове впровадження", "Почніть з одного важливого процесу, побачте результат і розширюйте систему крок за кроком."),
            ("refresh", "Підтримка й розвиток", "Після запуску ми підтримуємо та вдосконалюємо продукт на погоджених умовах."),
        ],
        "p6_eyebrow": "05 — Працюймо разом",
        "p6_title": "Як ми працюємо",
        "steps": [
            ("Обговорення задачі", "Коротка розмова про ваш бізнес і цілі."),
            ("Аналіз потреб", "Визначаємо процеси й те, що варто автоматизувати першим."),
            ("Рішення й вартість", "Чітка пропозиція: обсяг робіт, строки та ціна."),
            ("Розробка й тестування", "Регулярні демонстрації, щоб ви бачили прогрес."),
            ("Запуск і розвиток", "Запускаємо систему, навчаємо команду й продовжуємо вдосконалення."),
        ],
        "models_label": "Формати співпраці",
        "models": [
            ("Індивідуальний проєкт", "Рішення з нуля під вашу конкретну задачу."),
            ("Щомісячна підписка", "Окремі послуги та продукти доступні за щомісячним планом."),
        ],
        "cta_a": "Маєте ідею або бізнес-проблему, яку хочете автоматизувати?",
        "cta_b": "Обговорімо рішення.",
        "cta_note": "Напишіть нам — ми відповімо та підберемо зручний час для консультації.",
        "contact_labels": {"whatsapp": "WhatsApp", "telegram": "Telegram", "email": "Email", "website": "Сайт"},
        "contact_placeholders": {"whatsapp": "ваш номер WhatsApp", "telegram": "@username", "email": "name@company.com", "website": "vash-sait.com"},
        "ui_download_pdf": "Завантажити PDF",
        "ui_whatsapp_chat": "Написати у WhatsApp",
        "ui_edit": "Редагувати",
        "ui_more_projects": "Ще проєкти",
        "ui_view_portfolio": "Переглянути портфоліо",
        "word_empty_portfolio": "Додайте перший проєкт через редактор на сайті.",
        "word_empty_contacts": "Додайте контакти через редактор на сайті.",
        "word_contacts_label": "Контакти",
    },
    # ------------------------------------------------------------------ GERMAN
    "de": {
        "lang": "de",
        "descriptor": "Unabhängiges Softwarestudio",
        "doc_label": "Unternehmensprofil",
        "year": "2026",
        "cover_chip": "Unternehmensprofil · 2026",
        "cover_eyebrow": "Software · KI · Automatisierung",
        "cover_title_a": "Digitale Lösungen, die",
        "cover_title_b": "für Ihr Unternehmen arbeiten",
        "cover_sub": "Softwareentwicklung • KI-Automatisierung • Geschäftslösungen",
        "cover_lead": "Unabhängige Entwicklung von CRM-Systemen, Webplattformen, KI-Assistenten und Geschäftsautomatisierung — zugeschnitten auf die tatsächlichen Abläufe Ihres Unternehmens.",
        "cover_products_label": "Unsere aktiven Produkte",
        "p2_eyebrow": "01 — Über uns",
        "p2_title_a": "Ihr Unternehmen wächst.",
        "p2_title_b": "Manuelle Arbeit sollte nicht mitwachsen.",
        "p2_lead": "Wir sind ein unabhängiges Softwarestudio. Wir entwickeln CRM-Systeme, Webplattformen, KI-Assistenten und Automatisierungen — passend zu Ihrem Unternehmen, nicht umgekehrt.",
        "p2_problems_label": "Wo Zeit verloren geht",
        "p2_problems": [
            ("Daten sind überall verstreut", "Kunden in Excel, Gespräche in WhatsApp, Aufgaben nur im Kopf. Informationen gehen zwischen den Werkzeugen verloren."),
            ("Jeden Tag dieselbe Arbeit", "Gleiche Fragen beantworten, Daten kopieren sowie Dokumente und Berichte manuell erstellen."),
            ("Langsame Antworten, verlorene Kunden", "Wenn eine Anfrage erst Stunden später beantwortet wird, wählt der Interessent möglicherweise die Konkurrenz."),
        ],
        "p2_flow_label": "So kann es stattdessen laufen",
        "p2_flow": [
            ("Neue Anfrage", "Website, WhatsApp, Telegram"),
            ("KI-Assistent", "antwortet und erfasst Daten"),
            ("Im CRM gespeichert", "Kundenkarte wird automatisch angelegt"),
            ("Aufgabe für das Team", "mit Verantwortlichem und Frist"),
            ("Automatische Erinnerung", "nichts geht verloren"),
        ],
        "p2_cmp_label": "Warum eine individuelle Lösung?",
        "p2_cmp_head": ("Fertige Software", "Individuelle Lösung"),
        "p2_cmp": [
            ("Sie zahlen für Funktionen, die Sie nie nutzen", "Nur Funktionen, die Ihr Unternehmen braucht"),
            ("Ihr Team passt sich der Software an", "Die Software folgt Ihren Prozessen"),
            ("Die Anbindung an andere Systeme ist schwierig", "Angebunden an die Dienste, die Sie bereits nutzen"),
        ],
        "p3_eyebrow": "02 — Unsere Produkte",
        "p3_title": "Echte Produkte — von uns konzipiert, entwickelt und gestartet.",
        "p3_title_continued": "Weitere Produkte für reale Geschäftsanforderungen.",
        "p3_lead": "Jedes Produkt entstand aus einem praktischen Geschäftsproblem. Diese Erfahrung fließt in jedes individuelle Projekt ein.",
        "benefit_label": "Geschäftlicher Nutzen",
        "p4_eyebrow": "03 — Was wir entwickeln",
        "p4_title": "Was wir für Ihr Unternehmen entwickeln können",
        "p4_lead": "Wir beginnen mit dem gewünschten Ergebnis und wählen erst dann die passende Technologie.",
        "example_label": "Zum Beispiel",
        "services": [
            ("crm", "CRM & Unternehmensführung", "Alle Kunden, Geschäfte und Aufgaben an einem Ort. Sie sehen jederzeit, was im Unternehmen passiert.", "Vertriebspipeline, Teamaufgaben, Inhaber-Dashboard"),
            ("bot", "KI-Assistenten & Chatbots", "Beantworten häufige Fragen rund um die Uhr, erfassen Kundendaten und übergeben fertige Anfragen an Ihr Team.", "WhatsApp- / Telegram-Bots, Website-Chat. KI-Sprachassistent — in Entwicklung"),
            ("zap", "Geschäftsprozess-Automatisierung", "Wiederkehrende Aufgaben laufen selbstständig: Erinnerungen, Benachrichtigungen, Berichte und Datenübertragung.", "Automatische Follow-ups, Tagesberichte, Dokumenterstellung"),
            ("globe", "Websites & Webanwendungen", "Eine schnelle, moderne Website, die Kundenanfragen direkt in Ihr System überträgt.", "Unternehmenswebsite, Produktkatalog, Kundenportal"),
            ("code", "Individuelle Softwareentwicklung", "Software für Ihre genauen Abläufe, wenn Standardlösungen nicht passen.", "Interne Systeme, Buchung, Lagerverwaltung, Preisrechner"),
            ("link", "API- & Systemintegrationen", "Ihre Anwendungen tauschen Daten aus — kein manuelles Kopieren mehr.", "CRM + Messenger + Zahlungen + Tabellen"),
        ],
        "p5_eyebrow": "04 — Warum wir",
        "p5_title_a": "Die richtige Technologie,",
        "p5_title_b": "mit persönlicher Betreuung.",
        "p5_lead": "Sie arbeiten direkt mit dem Entwickler, der Ihr Produkt baut — ohne zusätzliche Managementebenen.",
        "p5_phases_label": "Schrittweise Einführung",
        "p5_phases": [
            ("Phase 1", "Kern", "Ein zentraler Prozess wird automatisiert"),
            ("Phase 2", "Integrationen", "Anbindung der Werkzeuge, die Sie bereits nutzen"),
            ("Phase 3", "KI & Skalierung", "Assistenten, Analysen, neue Funktionen"),
        ],
        "benefits": [
            ("target", "Auf Sie zugeschnitten", "Keine aufgezwungenen Vorlagen. Wir analysieren Ihre Prozesse und bauen genau das, was gebraucht wird."),
            ("sliders", "Direkt und flexibel", "Sie sprechen direkt mit dem Entwickler. Entscheidungen fallen schnell, Änderungen lassen sich leicht besprechen."),
            ("check", "Durch echte Produkte belegt", "Rieltix, Mapest und Forma sind live — Sie sehen die Qualität vor dem Start."),
            ("wallet", "Angemessenes Budget", "Nur benötigte Funktionen, ohne den Aufwand einer großen Agentur. Als Projekt oder monatlich."),
            ("layers", "Schrittweise Umsetzung", "Beginnen Sie mit einem wichtigen Prozess, sehen Sie das Ergebnis und erweitern Sie anschließend."),
            ("refresh", "Support & Weiterentwicklung", "Nach dem Start betreuen und verbessern wir das Produkt zu vereinbarten Bedingungen."),
        ],
        "p6_eyebrow": "05 — Gemeinsam starten",
        "p6_title": "So arbeiten wir",
        "steps": [
            ("Aufgabe besprechen", "Ein kurzes Gespräch über Ihr Unternehmen und Ihre Ziele."),
            ("Bedarf analysieren", "Wir erfassen die Prozesse und legen fest, was zuerst automatisiert wird."),
            ("Lösung & Kosten", "Ein klares Angebot: Umfang, Zeitplan und Preis."),
            ("Entwickeln & testen", "Regelmäßige Demos, damit Sie den Fortschritt immer sehen."),
            ("Starten & ausbauen", "Livegang, Team-Schulung und kontinuierliche Weiterentwicklung."),
        ],
        "models_label": "Formen der Zusammenarbeit",
        "models": [
            ("Individuelles Projekt", "Eine Lösung von Grund auf für Ihre spezifische Aufgabe."),
            ("Monatliches Abo", "Ausgewählte Leistungen und Produkte sind im Monatsplan verfügbar."),
        ],
        "cta_a": "Sie haben eine Idee oder ein Geschäftsproblem, das automatisiert werden soll?",
        "cta_b": "Sprechen wir über die Lösung.",
        "cta_note": "Schreiben Sie uns — wir antworten und finden einen passenden Termin für ein Beratungsgespräch.",
        "contact_labels": {"whatsapp": "WhatsApp", "telegram": "Telegram", "email": "E-Mail", "website": "Website"},
        "contact_placeholders": {"whatsapp": "Ihre WhatsApp-Nummer", "telegram": "@username", "email": "name@unternehmen.de", "website": "ihre-website.de"},
        "ui_download_pdf": "PDF herunterladen",
        "ui_whatsapp_chat": "WhatsApp-Chat",
        "ui_edit": "Bearbeiten",
        "ui_more_projects": "Weitere Projekte",
        "ui_view_portfolio": "Portfolio ansehen",
        "word_empty_portfolio": "Fügen Sie das erste Projekt über den Website-Editor hinzu.",
        "word_empty_contacts": "Fügen Sie Ihre Kontaktdaten über den Website-Editor hinzu.",
        "word_contacts_label": "Kontakt",
    },
    # ----------------------------------------------------------------- SPANISH
    "es": {
        "lang": "es",
        "descriptor": "Estudio independiente de software",
        "doc_label": "Perfil de la empresa",
        "year": "2026",
        "cover_chip": "Perfil de la empresa · 2026",
        "cover_eyebrow": "Software · IA · Automatización",
        "cover_title_a": "Soluciones digitales",
        "cover_title_b": "que trabajan para tu negocio",
        "cover_sub": "Desarrollo de software • Automatización con IA • Soluciones de negocio",
        "cover_lead": "Desarrollo independiente de sistemas CRM, plataformas web, asistentes de IA y automatización empresarial, adaptados al funcionamiento real de tu empresa.",
        "cover_products_label": "Nuestros productos activos",
        "p2_eyebrow": "01 — Quiénes somos",
        "p2_title_a": "Tu negocio crece.",
        "p2_title_b": "El trabajo manual no tiene por qué crecer con él.",
        "p2_lead": "Somos un estudio independiente de desarrollo de software. Creamos sistemas CRM, plataformas web, asistentes de IA y automatizaciones adaptadas a tu negocio, no al contrario.",
        "p2_problems_label": "Dónde se pierde el tiempo",
        "p2_problems": [
            ("Los datos están repartidos", "Clientes en Excel, conversaciones en WhatsApp y tareas en la cabeza. La información se pierde entre herramientas."),
            ("El mismo trabajo cada día", "Responder las mismas preguntas, copiar datos y preparar documentos e informes a mano."),
            ("Respuestas lentas y clientes perdidos", "Si una consulta tarda horas en responderse, el cliente potencial puede elegir a un competidor."),
        ],
        "p2_flow_label": "Así podría funcionar en su lugar",
        "p2_flow": [
            ("Nueva consulta", "web, WhatsApp, Telegram"),
            ("Asistente de IA", "responde y recoge los datos"),
            ("Guardado en el CRM", "la ficha del cliente se crea sola"),
            ("Tarea para el equipo", "con responsable y plazo"),
            ("Recordatorio automático", "nada queda olvidado"),
        ],
        "p2_cmp_label": "¿Por qué una solución a medida?",
        "p2_cmp_head": ("Software estándar", "Solución a medida"),
        "p2_cmp": [
            ("Pagas por funciones que nunca usas", "Solo las funciones que necesita tu negocio"),
            ("Tu equipo se adapta al software", "El software sigue tus procesos"),
            ("La conexión con otras herramientas es difícil", "Integrado con los servicios que ya usas"),
        ],
        "p3_eyebrow": "02 — Nuestros productos",
        "p3_title": "Productos reales diseñados, desarrollados y lanzados por nosotros.",
        "p3_title_continued": "Más productos para necesidades reales de negocio.",
        "p3_lead": "Cada producto nació de un problema empresarial práctico. Aportamos esa misma experiencia a cada proyecto a medida.",
        "benefit_label": "Valor para el negocio",
        "p4_eyebrow": "03 — Qué creamos",
        "p4_title": "Qué podemos crear para tu negocio",
        "p4_lead": "Partimos del resultado que necesitas y después elegimos la tecnología.",
        "example_label": "Por ejemplo",
        "services": [
            ("crm", "CRM y gestión empresarial", "Todos los clientes, oportunidades y tareas en un solo lugar. Puedes ver qué ocurre en tu negocio en cualquier momento.", "Embudo de ventas, tareas del equipo, panel del propietario"),
            ("bot", "Asistentes de IA y chatbots", "Responden preguntas habituales 24/7, recopilan datos del cliente y envían solicitudes completas a tu equipo.", "Bots de WhatsApp / Telegram, chat web. Asistente de voz con IA — en desarrollo"),
            ("zap", "Automatización de procesos", "Las tareas repetitivas se ejecutan solas: recordatorios, avisos, informes y traslado de datos.", "Seguimientos automáticos, informes diarios, generación de documentos"),
            ("globe", "Websites y aplicaciones web", "Una web rápida y moderna que envía las solicitudes del cliente directamente a tu sistema.", "Web corporativa, catálogo de productos, portal de clientes"),
            ("code", "Desarrollo de software a medida", "Software creado para tus procesos exactos cuando las herramientas estándar no encajan.", "Sistemas internos, reservas, inventario, calculadoras de precios"),
            ("link", "API e integraciones", "Tus aplicaciones intercambian datos: no más copias manuales.", "CRM + mensajería + pagos + hojas de cálculo"),
        ],
        "p5_eyebrow": "04 — Por qué elegirnos",
        "p5_title_a": "La tecnología adecuada,",
        "p5_title_b": "con un trato personal.",
        "p5_lead": "Trabajas directamente con el desarrollador que crea tu producto, sin capas intermedias de gestores.",
        "p5_phases_label": "Implantación por etapas",
        "p5_phases": [
            ("Fase 1", "Núcleo", "Se automatiza un proceso clave"),
            ("Fase 2", "Integraciones", "Conectamos las herramientas que ya usas"),
            ("Fase 3", "IA y escala", "Asistentes, análisis y nuevas funciones"),
        ],
        "benefits": [
            ("target", "Creado a tu medida", "Sin plantillas impuestas. Estudiamos tu proceso y creamos exactamente lo que necesita."),
            ("sliders", "Directo y flexible", "Hablas directamente con el desarrollador. Las decisiones son rápidas y los cambios se debaten con facilidad."),
            ("check", "Avalado por productos reales", "Rieltix, Mapest y Forma ya funcionan: puedes ver la calidad antes de empezar."),
            ("wallet", "Presupuesto razonable", "Solo las funciones que necesitas, sin los costes adicionales de una gran agencia. Por proyecto o mensual."),
            ("layers", "Implementación gradual", "Empieza por un proceso importante, comprueba el resultado y amplía paso a paso."),
            ("refresh", "Soporte y evolución", "Tras el lanzamiento mantenemos y mejoramos el producto según las condiciones acordadas."),
        ],
        "p6_eyebrow": "05 — Trabajemos juntos",
        "p6_title": "Cómo trabajamos",
        "steps": [
            ("Hablamos de la necesidad", "Una conversación breve sobre tu negocio y tus objetivos."),
            ("Analizamos los requisitos", "Mapeamos el proceso y decidimos qué automatizar primero."),
            ("Solución y coste", "Una propuesta clara: alcance, calendario y precio."),
            ("Desarrollo y pruebas", "Demos periódicas para que veas siempre el avance."),
            ("Lanzamiento y crecimiento", "Ponemos el sistema en marcha, formamos al equipo y seguimos mejorando."),
        ],
        "models_label": "Formas de colaboración",
        "models": [
            ("Proyecto a medida", "Una solución creada desde cero para tu necesidad concreta."),
            ("Suscripción mensual", "Algunos servicios y productos están disponibles con una cuota mensual."),
        ],
        "cta_a": "¿Tienes una idea o un problema de negocio que quieres automatizar?",
        "cta_b": "Hablemos de la solución.",
        "cta_note": "Escríbenos y te responderemos para acordar un horario cómodo para la consulta.",
        "contact_labels": {"whatsapp": "WhatsApp", "telegram": "Telegram", "email": "Correo", "website": "Web"},
        "contact_placeholders": {"whatsapp": "tu número de WhatsApp", "telegram": "@username", "email": "nombre@empresa.com", "website": "tu-web.com"},
        "ui_download_pdf": "Descargar PDF",
        "ui_whatsapp_chat": "Hablar por WhatsApp",
        "ui_edit": "Editar",
        "ui_more_projects": "Más proyectos",
        "ui_view_portfolio": "Ver portafolio",
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

