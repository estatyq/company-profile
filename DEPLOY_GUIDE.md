# Company Profile: сайт, админка и новые языки

Проект теперь работает как полноценный сайт с серверным редактированием. Контент хранится на сервере и сразу появляется у посетителей после нажатия **«Сохранить изменения»**.

## Быстрый запуск

Установите зависимости один раз:

```powershell
python -m pip install -r requirements.txt
```

Запустите сервер:

```powershell
powershell -ExecutionPolicy Bypass -File .\start_admin.ps1
```

Откройте:

- сайт: `http://127.0.0.1:8765/`;
- админка: `http://127.0.0.1:8765/admin`.

При первом локальном входе `/admin` предложит создать пароль. Введите не менее 10 символов. Пароль хранится только в виде хеша в `data/admin.json`.

## Что можно редактировать

В `/admin` доступны:

- название студии;
- WhatsApp, Telegram, email и сайт;
- основные заголовки и тексты для каждого языка;
- добавление, удаление и редактирование проектов;
- загрузка новых скриншотов;
- изменение пароля администратора.

Название, ссылка, статус, короткая категория и скриншот проекта синхронизируются между языками. Описание, ключевые возможности и ценность проекта редактируются отдельно для каждого языка.

После сохранения:

- `data/profile.json` становится основной серверной копией;
- `site/profile-en.json`, `site/profile-id.json`, `site/profile-uk.json`, `site/profile-de.json` и `site/profile-es.json` обновляются автоматически;
- предыдущая версия попадает в `data/backups/`;
- новые скриншоты сохраняются в `site/assets/web/uploads/`.

## Языки сайта

Сейчас доступны пять языков:

- English — `index.html`;
- Bahasa Indonesia — `id.html`;
- Українська — `uk.html`;
- Deutsch — `de.html`;
- Español — `es.html`.

При первом посещении сайт показывает выбор языка. Выбор запоминается в браузере, а позже язык можно изменить в верхней панели.

### Как добавить новый язык

Система языков находится в `content.py`.

1. Добавьте язык в словарь `LANGUAGES`:

```python
"fr": {
    "label": "FR",
    "native": "Français",
    "html": "fr.html",
    "file_suffix": "FR",
},
```

2. Добавьте перевод в `T["fr"]`. Необязательные ключи автоматически берутся из английской версии.

3. Для проектов добавьте ключ `"fr"` в поля `status`, `cover_sub`, `tag`, `features` и `benefit`. Если перевода пока нет, используется английский текст.

4. Пересоберите сайт:

```powershell
python build.py
```

После этого автоматически появятся:

- `site/fr.html`;
- `site/profile-fr.json`;
- `Company_Profile_FR.pdf`;
- `Company_Profile_FR.docx`;
- новый язык в переключателе сайта и в `/admin`.

Проверить полноту переводов можно командой:

```powershell
python tools\check_languages.py
```

## Экспорт

Кнопка **PDF** открывает системный диалог печати. Выберите **«Сохранить как PDF»**.

Кнопка **Word** скачивает настоящий `.docx`, сформированный из текущих данных сайта.

Готовые статические версии также создаются командой `python build.py` в папках `output/` и `site/`.

## Поисковая индексация

Сайт публикует:

- `https://xcombine.xyz/robots.txt`;
- `https://xcombine.xyz/sitemap.xml`;
- canonical-ссылки для каждого языка;
- hreflang-связи между пятью языковыми версиями;
- Open Graph и Twitter-разметку;
- структурированные данные `ProfessionalService`.

Панель `/admin` и её API закрыты от индексации через `robots.txt`.

После публикации добавьте сайт в поисковые системы:

1. **Google Search Console** → Add property → Domain → `xcombine.xyz`.
2. Подтвердите домен через DNS TXT-запись в Cloudflare.
3. Откройте **Sitemaps** и добавьте `sitemap.xml`.
4. Используйте **URL Inspection** для `https://xcombine.xyz/`.
5. В **Bing Webmaster Tools** импортируйте сайт из Google Search Console или добавьте его вручную.
6. При желании добавьте `xcombine.xyz` в Яндекс Вебмастер.

Cloudflare не должен блокировать поисковых роботов правилами WAF или Bot Fight Mode. В robots-файле уже разрешён обход публичных страниц.

## Публикация в интернете

Для `/admin` нужен Python-сервер. Обычный статический хостинг не сохранит изменения, поскольку браузер не имеет доступа к файлам сервера.

Подойдут VPS, Railway, Render, Fly.io или другой хостинг с постоянным диском и Python.

### Переменные окружения

Перед публикацией обязательно задайте:

```text
ADMIN_PASSWORD=надёжный-пароль-не-короче-12-символов
SECRET_KEY=случайная-длинная-строка
COOKIE_SECURE=1
HOST=0.0.0.0
PORT=8765
TRUST_PROXY=1
```

При заданном `ADMIN_PASSWORD` первый удалённый посетитель не сможет назначить себя администратором. Локальная первичная настройка пароля через `/admin` при этом отключается.

Запуск через production-сервер:

```powershell
waitress-serve --listen=0.0.0.0:8765 app:app
```

На Linux также можно использовать Gunicorn:

```bash
gunicorn --bind 0.0.0.0:8765 --workers 2 app:app
```

Используйте HTTPS. Если сайт работает за обратным прокси, передайте реальный IP клиента и включите защищённые cookies.

## Переключение через PM2

Рекомендуемая схема: сначала запустить новый сайт на отдельном внутреннем порту и проверить его, а старый проект остановить только после успешной проверки.

### Первый запуск

```bash
cd /var/www
git clone https://github.com/estatyq/company-profile.git
cd company-profile
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env
chmod 600 .env
mkdir -p data/backups site/assets/web/uploads
pm2 start ecosystem.config.cjs
pm2 logs company-profile --lines 100
```

В `.env` задайте:

```env
ADMIN_PASSWORD=длинный-уникальный-пароль
SECRET_KEY=случайная-строка-минимум-32-символа
COOKIE_SECURE=1
HOST=127.0.0.1
PORT=8765
TRUST_PROXY=1
```

Проверьте приложение до переключения домена:

```bash
curl -I http://127.0.0.1:8765/
curl -I http://127.0.0.1:8765/admin
```

Если `COOKIE_SECURE=1`, временный тест должен выполняться через HTTPS. Для теста по обычному HTTP временно поставьте `COOKIE_SECURE=0`, а после подключения TLS верните `1`.

### Остановка старого проекта

Посмотрите список процессов:

```bash
pm2 list
```

Не удаляйте старый проект сразу. Сначала остановите его по имени, чтобы освободить домен:

```bash
pm2 stop ИМЯ_СТАРОГО_ПРОЦЕССА
```

После проверки нового сайта сохраните состояние:

```bash
pm2 save
pm2 startup
```

`pm2 startup` выведет команду с `sudo` — выполните её, чтобы сайт запускался после перезагрузки сервера.

### Обновление после git push

```bash
cd /var/www/company-profile
git pull --ff-only origin main
.venv/bin/pip install -r requirements.txt
pm2 startOrReload ecosystem.config.cjs --update-env
pm2 save
```

### Nginx

Приложение слушает только `127.0.0.1:8765`. Nginx должен проксировать на него домен:

```nginx
server {
    listen 80;
    server_name xcombine.xyz www.xcombine.xyz;

    client_max_body_size 12m;

    location / {
        proxy_pass http://127.0.0.1:8765;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Проверьте и перезагрузите Nginx:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

Затем выпустите HTTPS-сертификат:

```bash
sudo certbot --nginx -d xcombine.xyz -d www.xcombine.xyz
```

### Что должно сохраняться между перезапусками

Обязательно храните на постоянном диске:

- `data/` — пароль, контент и резервные копии;
- `site/assets/web/uploads/` — загруженные скриншоты;
- `site/*.json` — опубликованные языковые данные.

Без постоянного диска изменения и загруженные файлы исчезнут после перезапуска контейнера.

## Безопасность

- Пароль хранится как scrypt-хеш.
- Для входа и API используются защищённые сессионные cookies.
- Запросы на изменение защищены CSRF-токеном.
- Вход ограничен по числу попыток.
- Загружаются только проверенные JPG, PNG и WebP.
- Изображения уменьшаются до 1600 × 1000 и сохраняются как оптимизированный JPEG.
- Поисковые системы не индексируют `/admin`.

Если пароль утерян в локальной версии:

1. Остановите сервер.
2. Удалите `data/admin.json`.
3. Запустите сервер и снова откройте `/admin`.

Для пересборки PDF и Word нужен установленный Chrome.
