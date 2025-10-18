# 🧭 KI Tools Web

**KI Tools Web** ist eine moderne, datengetriebene Webplattform rund um das Thema **Künstliche Intelligenz**.  
Ziel ist es, interessierten Anwendern – von Einsteigern bis zu Experten – einen strukturierten, redaktionell gepflegten
Überblick über KI-Tools, Anwendungsfälle, Prompts, Leitfäden und Vergleiche zu bieten.

Das Projekt ist vollständig **Open-Source** und auf **Django 5 + TailwindCSS + DaisyUI** aufgebaut.  
Die Plattform kombiniert redaktionelle Inhalte mit interaktiven Komponenten wie einem geführten Starter-Guide,
Kategorien-Filtern, Tool-Vergleichen und dynamischen Teaser-Sektionen.

---

## 🚀 Technischer Überblick

- **Framework:** Django 5.2 + Python 3.12
- **Frontend:** TailwindCSS + DaisyUI + Heroicons
- **Mehrsprachigkeit:** Deutsch / Englisch via `i18n_patterns`
- **Strukturierte Inhalte:** eigene Django-Apps für `catalog`, `content`, `compare`, `starter`, `newsletter`
- **CMS-Funktionalität:** alle Inhalte sind über das Django-Admin Interface pflegbar
- **Design-Philosophie:** minimalistisches, modulares Design mit Fokus auf Lesbarkeit und klaren Nutzerpfaden

---

## 💡 Zielgruppe

KI Tools Web richtet sich an:

- **Einsteiger** und **Interessierte**, die einen verständlichen Einstieg ins Thema KI suchen,
- **Technisch Versierte** (z. B. Entwickler, Studierende, Selbstständige), die Tools und Workflows vergleichen möchten,
- **Fachanwender**, die konkrete Anwendungsfälle und Prompts finden möchten, um eigene Aufgaben zu automatisieren.
- **Fachautoren**, die Wissen vermitteln möchten und redaktionelle Inhalte erstellen und überprüfen.

---

## 🧱 Webseitenkonzept

Das gesamte Konzept orientiert sich an drei Leitprinzipien:

> **Einfachheit · Transparenz · Struktur**

Die Website bietet sofortigen Zugang zu Inhalten, ohne Anmeldung oder Barrieren, und führt Besucher schrittweise in die
Themenwelt ein.

### 1. Startseite

Die **Home-Page** ist als Einstiegspunkt und thematische Orientierung konzipiert.

**Aufbau:**

1. **Kurze Einleitung / Hero-Text**  
   – vermittelt Zweck und Nutzen der Seite in einem Satz.  
   – präsentiert klar den Mehrwert („Finde das passende KI-Tool, lerne die Grundlagen oder starte mit einem Leitfaden“).

2. **Prominente Einstiegskarten**  
   – visuell prägnante Kacheln zu den Hauptbereichen:
    - 🔹 **Starter-Guide** – geführter Einstieg für Neulinge
    - 🔹 **Tool-Katalog** – alle Tools mit Filtern & Kategorien
    - 🔹 **Vergleiche** – Gegenüberstellungen („X vs Y“)
    - 🔹 **Guides** – redaktionelle Artikel mit Praxisbezug
    - 🔹 **Prompts** – Sammlungen für konkrete Aufgaben
    - 🔹 **Use-Cases** – reale Anwendungsbeispiele

3. **Empfohlene Tools (Featured Section)**  
   – ausgewählte Tools aus dem Katalog, redaktionell markiert (`is_featured=True`).  
   – visuelle Karten mit Logo, Kurzbeschreibung und Direktlink.

4. **Aktuelle Inhalte**  
   – dynamischer Mix aus Guides, Prompts und Use-Cases.  
   – automatische Balance (3/2/1-Verteilung) für gleichmäßige Darstellung.  
   – Karten mit Datum, Kategorie-Badge, Titel, Kurztext.

5. **Empfohlene Vergleiche**  
   – Teaser zu den neuesten oder populärsten Tool-Vergleichen.

6. **Newsletter-Call-to-Action** *(optional)*  
   – Eintrag für Neuigkeiten, Tools & Artikel (Double-Opt-In-fähig).

7. **Footer & Navigation**  
   – klare Struktur mit Themen, Sprache, Datenschutz und Impressum.

---

### 2. Starter-Guide (🧭 Geführter Einstieg)

Der **Starter-Guide** ist das Herzstück für neue Besucher.  
Er bietet einen sanften, geführten Einstieg in das Thema Künstliche Intelligenz, ohne technische Vorkenntnisse zu
verlangen.

**Konzept:**

- **Kein Login, keine Registrierung.**  
  Alle Besucher können frei darauf zugreifen.

- **Zwei Modi:**
    1. **Direkter Einstieg** – Besucher klicken einfach auf „Starter-Guide“.
    2. **Kurzer Fragen-Check (3 Fragen)** – optional, um einen individuellen Leitfaden zu erhalten.  
       → Antworten werden *nur lokal im Browser* gespeichert (kein Server-Profil, DSGVO-konform).

- **Inhaltliche Struktur:**
    - 3 – 6 Kapitel, z. B.:
        1. Was ist KI?
        2. Prompting-Grundlagen
        3. Erstes Tool im Einsatz
        4. Produktiver Arbeiten mit KI
        5. Automatisieren mit KI-Tools
        6. Eigenes Projekt starten
    - Jedes Kapitel besteht aus mehreren Kacheln (`StarterItem`), die redaktionell gepflegt werden können.

- **Pflege im Admin-Bereich:**
    - `StarterGuide` → Titel, Hero-Text, Einleitung
    - `StarterSection` → Kapitelüberschriften, Einleitungstexte
    - `StarterItem` → Verknüpfung mit internen Inhalten (Guides, Tools, Vergleiche) oder externen Links
    - Reihenfolge & Texte sind vollständig editierbar

**Technisch:**

- eigener App-Namespace `starter`
- Templates: `starter/index.html`, `starter/intro.html`
- Modelle: `StarterGuide`, `StarterSection`, `StarterItem`
- Client-seitige Empfehlung (LocalStorage), kein Tracking oder User-Profil
- Level-Cookie (`ktw_level`) speichert nur das ausgewählte **Anforderungslevel**

---

### 3. Anforderungslevel (Schieberegler „Starter | Fortgeschritten | Profi“)

- Positioniert **in der Navbar**.
- Speicherung als Cookie `ktw_level` (Laufzeit 180 Tage, keine personenbezogenen Daten).
- Beeinflusst:
    - Anzeige-Labels („Empfohlen für Starter“ etc.)
    - Sortierung/Filterung auf Inhaltsseiten (optional)
- Nutzer können jederzeit umschalten oder das Cookie löschen.
- Dadurch kann der Nutzer vermeiden, von anspruchsvollen Inhalten überfordert zu werden, oder die Start-Guides
  auszublenden.

---

### 4. Inhaltsbereiche

#### 🧩 Katalog (`catalog`)

- Tools mit Kategorien, Preismodellen und Affiliate-Infos
- Felder: Name, Beschreibung, Website, Preis, Sprachen, etc.
- M2M-Relation zu `Category`
- Admin-Inlines für `PricingTier` und `AffiliateProgram`
- „Featured Tools“ erscheinen auf der Startseite

#### 📚 Content (`content`)

- Basisklassen `Guide`, `Prompt`, `UseCase`
- Alle erben von `Publishable` (Status, Veröffentlichung, Manager `published`)
- Unterstützen Mehrsprachigkeit, Tagging und Kategorien
- Liefert Daten an Teaser- und Empfehlungsbereiche

#### ⚖️ Vergleiche (`compare`)

- Strukturierte Gegenüberstellungen von zwei oder mehr Tools
- Enthält JSON-basiertes `score_breakdown`
- Gewinner-Tool (`winner_id`) optional
- Darstellung als responsive Vergleichstabelle

#### 📰 Newsletter (`newsletter`)

- Optionaler Bereich für Abonnenten
- Modell `Subscriber(email, tags, created_at, double_opt_in)`

#### 🧭 Starter (`starter`)

- Siehe oben: CMS-gesteuerter Leitfaden für Einsteiger

---

### 5. Design & Benutzererlebnis

- **Designsystem:** DaisyUI 5 (basierend auf TailwindCSS 3)
- **Themes:** `light` (standard), `dracula` (prefers-dark)
- **Icons:** Heroicons v2
- **Komponenten:** Cards, Buttons, Badges, Dropdowns, modale Dialoge
- **Fokus auf Lesbarkeit:** großzügige Abstände, line-clamp für Textkonsistenz
- **Performance:** optimierte Bildgrößen, Template-Caching, minimaler JS-Einsatz

---

### 6. Datenschutz & Philosophie

- Kein Account, keine Registrierung, keine Tracking-Cookies.
- Einziger Cookie: `ktw_level` (Anforderungslevel, technisch notwendig).
- Optionale Nutzung von LocalStorage für personalisierte Empfehlungen im Starter-Guide.
- DSGVO-freundlich: keine personenbezogenen Daten, keine Weitergabe an Dritte.

---

## 🛠️ Status

- Das Projekt befindet sich aktuell in der Entwicklung.
- Ein Release termin ist noch nicht bekannt
