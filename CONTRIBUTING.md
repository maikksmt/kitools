# 🤝 Beiträge zu KI Tools Web

Willkommen bei **KI Tools Web** – und danke für dein Interesse, zum Projekt beizutragen!  
Diese Datei erklärt, **wie du mitarbeiten kannst**, **welche Regeln gelten**  
und **was rechtlich zu beachten ist**.

---

## 🧭 Grundprinzip

KI Tools Web ist eine **nicht-kommerzielle, quelloffene Plattform**  
zur Erkundung und zum Vergleich von KI-Tools, Anwendungsfällen und Leitfäden.

Du darfst gerne:

- Fehler oder Verbesserungsvorschläge melden (`Issues`)
- Code- oder Content-Verbesserungen vorschlagen (`Pull Requests`)
- neue Ideen für Inhalte, Layouts oder Features diskutieren

---

## ⚖️ Lizenz & rechtliche Hinweise

Dieses Projekt steht unter der  
[**PolyForm Noncommercial License 1.0.0**](https://polyformproject.org/licenses/noncommercial/1.0.0/).

Das bedeutet:

- 🔍 Du darfst den Code **ansehen, lernen und mitwirken**,  
  solange die Nutzung **nicht kommerziell** ist.
- 💼 **Kommerzielle oder private Wiederverwendung** ist **nicht erlaubt**  
  (z. B. in eigenen Produkten, Websites, SaaS-Angeboten oder Forks).
- 🧾 Alle Beiträge, die du einreichst (z. B. per Pull Request),  
  werden automatisch **unter derselben Lizenz** weitergegeben.

Durch das Einreichen eines Pull Requests stimmst du zu,
dass dein Beitrag unter der **PolyForm Noncommercial License 1.0.0**
im offiziellen Repository integriert werden darf.

---

## 🔧 Entwicklungsumgebung

### Voraussetzungen

- Python 3.12+
- Django 5.x
- Node.js + npm für Tailwind/DaisyUI Assets

### Lokaler Start

```bash
git clone https://github.com/<dein-github-username>/kitools-web.git
cd kitools-web
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Frontend (Tailwind/DaisyUI):

```bash
npm install
npm run dev
```

---

## 🧱 Code Style

- **Python:** PEP 8-konform (verwende `black` oder `ruff` für Formatierung)
- **Templates:** Django-Standard mit `i18n`-Blöcken für Mehrsprachigkeit
- **CSS:** Tailwind + DaisyUI-Komponenten (keine Inline-Styles)
- **Commit-Messages:** klar & beschreibend (z. B. `fix:`, `feat:`, `refactor:`)

Beispiel:

```
feat(starter): add section editing in admin
fix(compare): correct breadcrumb links
```

---

## 🧩 Branches & Pull Requests

- **main** → stabile, produktive Version
- **dev** → Entwicklungszweig für neue Features

Bitte erstelle Pull Requests gegen den Branch `dev`.

### Schritte:

1. Erstelle ein Issue, wenn du eine größere Änderung planst
2. Forke das Repo und arbeite auf einem eigenen Branch (`feature/...`)
3. Teste deine Änderungen lokal
4. Erstelle einen Pull Request gegen `dev`
5. Beschreibe kurz, **was du geändert hast und warum**

---

## 🧠 Inhalte (Content-Beiträge)

Wenn du redaktionelle Inhalte (z. B. neue Guides, Prompts oder Vergleiche) vorschlägst:

- nutze einfache, neutrale Sprache (kein Marketing)
- verlinke Quellen oder Tools seriös
- keine KI-generierten Texte ohne Review

---

## 🚫 Nicht erlaubt

- Kommerzielle Nutzung oder Integration in eigene Plattformen
- Automatische oder KI-basierte Massenbeiträge ohne Review
- Upload urheberrechtlich geschützter Materialien (z. B. Bilder, Logos)
- Veröffentlichung von personenbezogenen Daten

---

## 🧾 Hinweise zu Urheberrecht & Mitwirkung

Mit dem Einreichen eines Beitrags stimmst du folgenden Punkten zu:

1. Du bist der Urheber deiner Beiträge oder hast die Rechte daran.
2. Du überträgst dem Projekt-Inhaber ein einfaches, unbefristetes Nutzungsrecht,
   um deinen Beitrag in **KI Tools Web** zu verwenden.
3. Du erhältst keine Vergütung oder Gegenleistung.
4. Dein Beitrag bleibt unter der gleichen **PolyForm Noncommercial License 1.0.0** verfügbar.

---

## 💬 Kommunikation & Support

- **Bugs oder Feature-Wünsche:** GitHub Issues
- **Diskussionen & Feedback:** GitHub Discussions (wenn aktiviert)
- **Kontakt:** maik.kusmat@example.com

---

## 🙏 Danke!

Deine Unterstützung hilft, KI Tools Web weiterzuentwickeln  
und das Thema Künstliche Intelligenz verständlich und zugänglich zu machen.

> _„Open Knowledge – ohne Kommerz, für alle, die lernen und verstehen wollen.“_
