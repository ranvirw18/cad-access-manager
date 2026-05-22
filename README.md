# CAD Institute Launcher

Desktop launcher for institute lab PCs: students log in, the app validates a **50-day subscription**, then starts AutoCAD. Admins manage accounts locally with SQLite.

---

## Quick start

```powershell
cd d:\cad-access-manager
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

**Default admin:** `admin` / `admin123` — change after first use in `config/settings.py` or add a password-change feature later.

**AutoCAD path:** edit `AUTOCAD_EXE` in `config/settings.py`.

---

## 1. Software architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        main.py                               │
│                    (starts the app)                          │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                      ui/ (CustomTkinter)                     │
│   login_window.py  │  admin_window.py  │  app.py             │
└─────────────────────────┬───────────────────────────────────┘
                          │ calls
┌─────────────────────────▼───────────────────────────────────┐
│                    services/ (business logic)                │
│   auth_service.py  │  admin_service.py  │  autocad_launcher  │
└─────────────────────────┬───────────────────────────────────┘
                          │ uses
┌─────────────────────────▼───────────────────────────────────┐
│              repositories/ (database access)                 │
│        student_repository.py  │  admin_repository.py         │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│   database/ + models/ + utils/ (dates, bcrypt)               │
└─────────────────────────────────────────────────────────────┘
```

**Why layers?**

| Layer | Role | Beginner tip |
|-------|------|----------------|
| **UI** | Buttons, labels, screens only | No SQL or expiry math here |
| **Services** | Rules: login checks, launch CAD | Easy to unit-test later |
| **Repositories** | SQL INSERT/SELECT/UPDATE | One place to change DB |
| **Models** | `Student`, `Admin` objects | Cleaner than raw dict rows |
| **Utils** | Dates + passwords | Reused everywhere |

---

## 2. Folder structure

```
cad-access-manager/
├── main.py                 # Entry point
├── requirements.txt
├── config/
│   └── settings.py         # Paths, 50 days, AutoCAD exe, theme
├── database/
│   ├── schema.sql          # Table definitions
│   └── connection.py       # Open DB, run schema, seed admin
├── models/
│   ├── student.py
│   └── admin.py
├── repositories/
│   ├── student_repository.py
│   └── admin_repository.py
├── services/
│   ├── auth_service.py
│   ├── admin_service.py
│   └── autocad_launcher.py
├── utils/
│   ├── security.py         # bcrypt hash / verify
│   └── dates.py            # 50-day expiry logic
├── ui/
│   ├── app.py
│   ├── login_window.py
│   ├── admin_window.py
│   └── components/
│       └── message_dialog.py
└── data/
    └── cad_launcher.db     # Created at runtime (gitignored)
```

---

## 3. SQLite schema

**students**

| Column | Type | Purpose |
|--------|------|---------|
| id | INTEGER PK | Internal ID |
| username | TEXT UNIQUE | Login name (case-insensitive) |
| password_hash | TEXT | bcrypt hash, never plain text |
| join_date | TEXT (ISO) | Subscription start |
| expiry_date | TEXT (ISO) | join_date + 50 days |
| is_active | INTEGER 0/1 | Admin can disable without deleting |
| created_at / updated_at | TEXT | Audit (future) |

**admins**

| Column | Type | Purpose |
|--------|------|---------|
| id | INTEGER PK | |
| username | TEXT UNIQUE | Admin login |
| password_hash | TEXT | bcrypt |

---

## 4. MVP roadmap

| Phase | Goal | Status |
|-------|------|--------|
| **MVP-1** | DB + bcrypt + 50-day expiry + student login | Done in this repo |
| **MVP-2** | Admin CRUD (add/remove/password/extend/disable) | Done |
| **MVP-3** | AutoCAD launch + clear “Subscription Expired” | Done |
| **MVP-4** | PyInstaller `.exe`, lab deployment doc | See below |
| **MVP-5** | Hardening: change default admin password UI, logs | Next |
| **Future** | Online auth, JWT, attendance, device lock, cloud | Planned |

---

## 5. First files to create (order)

1. `config/settings.py` — constants
2. `database/schema.sql` + `connection.py`
3. `utils/security.py` + `utils/dates.py`
4. `models/student.py`
5. `repositories/student_repository.py`
6. `services/auth_service.py`
7. `ui/login_window.py` + `main.py`
8. Admin + launcher (already added in this scaffold)

---

## 6. First coding steps

1. Install dependencies and run `python main.py`.
2. Open **Admin Panel** → login `admin` / `admin123`.
3. **Add** a test student (username + password).
4. **Student Login** with that account → AutoCAD should start (if path is correct).
5. In admin, note **ID**, test **+30 days**, **Disable**, **Remove**.

To test expiry without waiting 50 days, temporarily set `join_date` in DB or add a test student with `join_date` 51 days ago via Python shell.

---

## 7. Expiry-date logic

Implemented in `utils/dates.py`:

```python
expiry_date = join_date + timedelta(days=50)

# Expired only AFTER expiry_date (last day of subscription still works)
is_expired = today() > expiry_date
```

`AuthService.login_student()` order:

1. User exists?
2. Password correct?
3. `is_active`?
4. Not expired? → else **Subscription Expired**
5. Success → UI launches AutoCAD

---

## 8. Admin workflow

```
Admin logs in
    → Add student (join_date = today, expiry = today + 50)
    → List shows ID, username, dates, days left, active ON/OFF
    → Select ID:
         • +30 days → extend_validity
         • Disable / Enable → is_active
         • New password → bcrypt re-hash
         • Remove → DELETE row
Student logs in
    → Same checks as above
    → Expired → modal "Subscription Expired" (no AutoCAD)
```

---

## 9. Build EXE (PyInstaller)

```powershell
pip install pyinstaller
pyinstaller --onefile --windowed --name "CAD Institute Launcher" main.py
```

Output: `dist/CAD Institute Launcher.exe`

**Tips:**

- Copy `data/` folder next to the exe on first run, or let the app create `data/cad_launcher.db` beside the exe (adjust `DATABASE_PATH` in settings if you bundle differently).
- Test on a clean lab PC without Python installed.
- Sign the exe later for fewer SmartScreen warnings (optional).

---

## 10. Future upgrades (hooks already in place)

| Feature | Where to extend |
|---------|-----------------|
| Online / JWT auth | New `services/remote_auth_service.py`, keep `AuthService` interface |
| Attendance | New table + `attendance_repository.py` |
| Device lock | Store machine ID in settings + validate on login |
| Multi-PC / cloud | Sync `students` via API; SQLite becomes local cache |
| Branding | `ui/` theme + logo in `assets/` |
| Stronger bypass protection | Windows startup policy, replace shell, group policy (IT topic) |

**Security ladder (gradual):**

1. bcrypt passwords (done)
2. Disable accounts without delete (done)
3. Hide DB from students (NTFS permissions on `data/`)
4. Launcher required at login (institute IT)
5. Later: server-side validation, device binding

---

## License

Internal institute use — adjust as needed.
