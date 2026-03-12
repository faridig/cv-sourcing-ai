# 🏗️ TECH_DEBT.md

Journal de la dette technique. Toute décision "rapide" ou divergence par rapport au `BACKLOG.md` (qui a été validée en raison de contraintes de temps ou de blocages techniques) doit être documentée ici par le Lead-Dev ou l'UX pour être traitée ultérieurement.

---

### [2026-03-12] - [Sprint 1]
**Dette contractée** : Fichiers liés aux outils internes (`.opencode`, `openrtk`) commités par erreur au Sprint 0 avant l'ajout au `.gitignore`.
**Raison** : Oubli initial dans le `.gitignore`. Les dossiers sont ignorés maintenant, mais toujours suivis par l'index Git.
**Impact** : Dépôt pollué, risque de conflits futurs avec les sessions locales.
**Action future à planifier** : Exécuter `git rm -r --cached .opencode openrtk` en début de Sprint 2 (tâche assignée).