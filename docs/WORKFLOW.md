# 🧩 Git-Workflow für KI Tools Web

Dieser Workflow definiert **Branches, Commits, Pull Requests, Releases und Hotfixes** für das Repository.
Er ist leichtgewichtig, GitHub-kompatibel und passt zu den Regeln in `CONTRIBUTING.md`.

---

## 1) Branch-Strategie

| Branch | Zweck |
|-------|------|
| `main` | Stabile, veröffentlichte Version (Produktionscode) |
| `dev` | Aktive Entwicklung – hier wird zusammengeführt und getestet |
| `feature/<kurz-beschreibung>` | Kurzlebige Branches für einzelne Tasks/Features |
| `hotfix/<beschreibung>` | Schnelle Fixes direkt aus `main`, die sofort veröffentlicht werden müssen |

**Regeln:**
- `main` wird **nur** über Pull Requests gemerged (kein direkter Push).
- Neue Arbeiten entstehen aus `dev` mit `feature/...` Branches.
- Nach Merge eines Features in `dev` wird dort getestet. Releases erfolgen durch Merge `dev → main`.

---

## 2) Typische Befehle

```bash
# Neues Feature starten
git checkout dev
git pull
git checkout -b feature/starter-guide

# Arbeiten committen
git add -A
git commit -m "feat(starter): add section editing in admin"
git push -u origin feature/starter-guide

# Pull Request erstellen (gegen dev)
# (dann auf GitHub PR öffnen)
```

---

## 3) Commit-Konvention (empfohlen)

Verwende prägnante, strukturierte Messages (angelehnt an Conventional Commits):

```
feat(starter): add section editing in admin
fix(compare): correct breadcrumb links
docs(readme): add project overview
refactor(content): simplify get_latest_items mix logic
chore(ci): add GitHub Actions cache for pip
```

**Typen:** `feat`, `fix`, `docs`, `refactor`, `test`, `build`, `chore`, `ci`

---

## 4) Pull Requests (PR)

**Ziel:** Qualität sichern, Änderungen nachvollziehbar machen.

**Checkliste vor dem PR:**
- [ ] Branch basiert auf aktuellem `dev`
- [ ] Lint/Format (z. B. `ruff`, `black`) ausgeführt
- [ ] Lokale Tests ok (`python manage.py test` falls vorhanden)
- [ ] Relevante Screenshots/Notizen angehängt
- [ ] Beschreibung: *Was* wurde geändert, *warum*, *wie getestet*

**Review-Regeln:**
- Mindestens 1 Review-Approval vor Merge in `dev`
- Squash & Merge empfohlen (saubere Historie)
- PR-Titel folgt Commit-Konvention

---

## 5) Rebase vs Merge

- **Feature aktualisieren:** `git fetch && git rebase origin/dev` (bevorzugt, lineare Historie)
- **Konflikte lösen**, weiter pushen mit `--force-with-lease`:
  ```bash
  git push --force-with-lease
  ```

---

## 6) Release-Prozess

1. `dev` ist grün (Tests ok, manuell geprüft).
2. Erstelle Release-PR: **`dev → main`**
3. PR-Titel: `release: vX.Y.Z` + Changelog im PR-Text
4. Merge in `main` → GitHub Release und Tag setzen (optional semver: `vX.Y.Z`)
5. Nach Release: `main` zurück nach `dev` mergen oder `dev` aus `main` rebasen

**SemVer-Konvention:**  
`MAJOR.MINOR.PATCH` – *Kompatibilitätsbrüche / Features / Bugfixes*

---

## 7) Hotfix-Flow (kritische Fehler)

```bash
# Aus main abzweigen
git checkout main
git pull
git checkout -b hotfix/<kurz-beschreibung>

# Fix erstellen & committen
git add -A
git commit -m "fix: <kurz-beschreibung>"
git push -u origin hotfix/<kurz-beschreibung>

# PR: hotfix → main (Review, schnell mergen)
# Danach: main → dev synchronisieren
git checkout dev
git pull
git merge main
git push
```

---

## 8) Tags & Changelog

- Release-Tags: `vX.Y.Z`
- Changelog im PR-Text oder in `CHANGELOG.md` pflegen (optional)
- Wichtige Änderungen stichpunktartig: Added / Changed / Fixed / Removed

---

## 9) CI-Empfehlungen (optional)

- GitHub Actions: Lint + Build + (später) Tests ausführen
- Workflows für PRs gegen `dev` und `main`
- Caching für Python/Node-Abhängigkeiten

---

## 10) Häufige Probleme

**Konflikte beim Merge/Rebase:**  
- Bearbeite Konfliktdateien, teste lokal, committe die Auflösung.
- Push mit `--force-with-lease` *nur* auf Feature-Branches (nie `main`/`dev`).

**„Diverged“ Branch:**  
- Nutze Rebase statt Merge (`git rebase origin/dev`), um Doppel-Commits zu vermeiden.

---

## 11) Namenskonventionen

- Features: `feature/<bereich>-<kurz>` → `feature/starter-admin-ui`
- Fixes: `fix/<bereich>-<kurz>` → `fix/compare-breadcrumb`
- Hotfix: `hotfix/<kurz>` → `hotfix/runtime-error-startup`

---

## 12) Rollen

- **Maintainer**: Review, Merge, Release, Branch-Schutzregeln
- **Contributor**: PRs erstellen, auf Feedback reagieren
- **Reviewer**: Code prüfen, Tests nachvollziehen, Feedback geben

---

## 13) Branch-Schutz (GitHub Settings)

- `main`: Require PR, Require review, Disallow force-push
- `dev`: Require PR, Require status checks, Disallow force-push

---

## 14) TL;DR (Kurzfassung)

1. Feature-Branch aus `dev` erstellen  
2. Arbeiten, Commits schreiben, PR gegen `dev` öffnen  
3. Review & Squash-Merge  
4. Release: `dev` → `main` via PR, taggen, changelog
