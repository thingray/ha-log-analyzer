# 📊 Home Assistant Log Analyzer

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![HA Version](https://img.shields.io/badge/Home%20Assistant-2023.1+-blue.svg)](https://www.home-assistant.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Languages](https://img.shields.io/badge/Languages-FR%20|%20EN%20|%20DE-green.svg)](#)

🇫🇷 **Français** | 🇬🇧 [English](#-english) | 🇩🇪 [Deutsch](#-deutsch)

---

## 🇫🇷 Français

Analyse automatique des logs Home Assistant avec rapport statistique des erreurs, groupées par intégration et triées par fréquence.

### ✨ Fonctionnalités

- **🌍 Multi-langue**: Français, Anglais, Allemand
- **🎯 Filtrage par sévérité**: CRITICAL, ERROR, WARNING
- **📦 Groupement par intégration**: Identifie quelles intégrations causent le plus de problèmes
- **🔝 Top 10 erreurs**: Les erreurs les plus fréquentes avec première/dernière occurrence
- **🧠 Normalisation intelligente**: Regroupe les erreurs similaires (UUIDs, IPs, timestamps masqués)
- **📊 Dashboard card**: Visualisation directe dans Home Assistant
- **⏰ Analyse automatique**: Programmable quotidiennement

### 📦 Installation via HACS (Recommandé)

1. Ouvrez **HACS** dans Home Assistant
2. Cliquez sur les 3 points en haut à droite → **Dépôts personnalisés**
3. Ajoutez l'URL: `https://github.com/VOTRE_USERNAME/ha-log-analyzer`
4. Catégorie: **Integration**
5. Cliquez **Ajouter**
6. Recherchez "HA Log Analyzer" et installez
7. Redémarrez Home Assistant

### 🔧 Installation manuelle

1. Créez le dossier `/config/scripts/` si inexistant:
   ```bash
   mkdir -p /config/scripts
   ```

2. Copiez `ha_log_analyzer.py` dans `/config/scripts/`

3. Ajoutez le contenu de `ha_config.yaml` à votre `configuration.yaml` ou créez un package:
   ```yaml
   # configuration.yaml
   homeassistant:
     packages:
       log_analyzer: !include packages/log_analyzer.yaml
   ```

4. Redémarrez Home Assistant

5. Ajoutez la card `dashboard_card.yaml` à votre dashboard

### 📖 Utilisation

1. **Sélectionnez votre langue** dans le dropdown du dashboard
2. **Cliquez "Analyser maintenant"** ou attendez l'analyse quotidienne (6h00)
3. **Consultez le rapport**:
   - Top erreurs par fréquence
   - Répartition par sévérité
   - Intégrations problématiques

### 🖥️ Utilisation en ligne de commande

```bash
# Français (défaut)
python3 /config/scripts/ha_log_analyzer.py /config/home-assistant.log fr

# English
python3 /config/scripts/ha_log_analyzer.py /config/home-assistant.log en

# Deutsch
python3 /config/scripts/ha_log_analyzer.py /config/home-assistant.log de
```

### 📊 Exemple de rapport

```
======================================================================
📊 HOME ASSISTANT LOG ANALYZER - RAPPORT
======================================================================
Généré le: 2026-02-01 14:30:00
Entrées totales analysées: 15234
Entrées filtrées (ERROR, WARNING, CRITICAL): 847

----------------------------------------------------------------------
📈 RÉSUMÉ PAR SÉVÉRITÉ
----------------------------------------------------------------------
  🔴 CRITICAL: 2
  🟠 ERROR: 156
  🟡 WARNING: 689

----------------------------------------------------------------------
📦 PAR INTÉGRATION
----------------------------------------------------------------------
  ezviz: 234 (ERROR: 12, WARNING: 222)
  haffmpeg: 89 (ERROR: 45, WARNING: 44)
  core: 52 (ERROR: 8, WARNING: 44)

----------------------------------------------------------------------
🔝 TOP 10 ERREURS PAR FRÉQUENCE
----------------------------------------------------------------------

  1. 🟠 [haffmpeg] x89
     Timeout reading image.
     Première: 2026-01-29 22:57:05 | Dernière: 2026-02-01 13:52:58
```

---

## 🇬🇧 English

Automatic Home Assistant log analysis with statistical error report, grouped by integration and sorted by frequency.

### ✨ Features

- **🌍 Multi-language**: French, English, German
- **🎯 Severity filtering**: CRITICAL, ERROR, WARNING
- **📦 Integration grouping**: Identifies which integrations cause the most problems
- **🔝 Top 10 errors**: Most frequent errors with first/last occurrence
- **🧠 Smart normalization**: Groups similar errors together (UUIDs, IPs, timestamps masked)
- **📊 Dashboard card**: Direct visualization in Home Assistant
- **⏰ Automatic analysis**: Daily scheduling available

### 📦 Installation via HACS (Recommended)

1. Open **HACS** in Home Assistant
2. Click the 3 dots in the top right → **Custom repositories**
3. Add URL: `https://github.com/YOUR_USERNAME/ha-log-analyzer`
4. Category: **Integration**
5. Click **Add**
6. Search for "HA Log Analyzer" and install
7. Restart Home Assistant

### 🔧 Manual Installation

1. Create the folder `/config/scripts/` if it doesn't exist:
   ```bash
   mkdir -p /config/scripts
   ```

2. Copy `ha_log_analyzer.py` to `/config/scripts/`

3. Add the content of `ha_config.yaml` to your `configuration.yaml` or create a package:
   ```yaml
   # configuration.yaml
   homeassistant:
     packages:
       log_analyzer: !include packages/log_analyzer.yaml
   ```

4. Restart Home Assistant

5. Add the `dashboard_card.yaml` card to your dashboard

### 📖 Usage

1. **Select your language** in the dashboard dropdown
2. **Click "Analyze now"** or wait for the daily analysis (6:00 AM)
3. **View the report**:
   - Top errors by frequency
   - Distribution by severity
   - Problematic integrations

### 🖥️ Command line usage

```bash
# Français (default)
python3 /config/scripts/ha_log_analyzer.py /config/home-assistant.log fr

# English
python3 /config/scripts/ha_log_analyzer.py /config/home-assistant.log en

# Deutsch
python3 /config/scripts/ha_log_analyzer.py /config/home-assistant.log de
```

---

## 🇩🇪 Deutsch

Automatische Home Assistant Log-Analyse mit statistischem Fehlerbericht, gruppiert nach Integration und sortiert nach Häufigkeit.

### ✨ Funktionen

- **🌍 Mehrsprachig**: Französisch, Englisch, Deutsch
- **🎯 Schweregradfilterung**: CRITICAL, ERROR, WARNING
- **📦 Integrationsgruppierung**: Identifiziert welche Integrationen die meisten Probleme verursachen
- **🔝 Top 10 Fehler**: Häufigste Fehler mit erstem/letztem Auftreten
- **🧠 Intelligente Normalisierung**: Gruppiert ähnliche Fehler (UUIDs, IPs, Zeitstempel maskiert)
- **📊 Dashboard-Karte**: Direkte Visualisierung in Home Assistant
- **⏰ Automatische Analyse**: Tägliche Planung verfügbar

### 📦 Installation über HACS (Empfohlen)

1. Öffnen Sie **HACS** in Home Assistant
2. Klicken Sie auf die 3 Punkte oben rechts → **Benutzerdefinierte Repositories**
3. URL hinzufügen: `https://github.com/IHR_USERNAME/ha-log-analyzer`
4. Kategorie: **Integration**
5. Klicken Sie **Hinzufügen**
6. Suchen Sie nach "HA Log Analyzer" und installieren Sie
7. Starten Sie Home Assistant neu

### 🔧 Manuelle Installation

1. Erstellen Sie den Ordner `/config/scripts/` falls nicht vorhanden:
   ```bash
   mkdir -p /config/scripts
   ```

2. Kopieren Sie `ha_log_analyzer.py` nach `/config/scripts/`

3. Fügen Sie den Inhalt von `ha_config.yaml` zu Ihrer `configuration.yaml` hinzu oder erstellen Sie ein Package:
   ```yaml
   # configuration.yaml
   homeassistant:
     packages:
       log_analyzer: !include packages/log_analyzer.yaml
   ```

4. Starten Sie Home Assistant neu

5. Fügen Sie die `dashboard_card.yaml` Karte zu Ihrem Dashboard hinzu

### 📖 Verwendung

1. **Wählen Sie Ihre Sprache** im Dashboard-Dropdown
2. **Klicken Sie auf "Jetzt analysieren"** oder warten Sie auf die tägliche Analyse (6:00 Uhr)
3. **Sehen Sie den Bericht**:
   - Top Fehler nach Häufigkeit
   - Verteilung nach Schweregrad
   - Problematische Integrationen

### 🖥️ Kommandozeilenverwendung

```bash
# Français (Standard)
python3 /config/scripts/ha_log_analyzer.py /config/home-assistant.log fr

# English
python3 /config/scripts/ha_log_analyzer.py /config/home-assistant.log en

# Deutsch
python3 /config/scripts/ha_log_analyzer.py /config/home-assistant.log de
```

---

## 📁 Structure des fichiers / File Structure / Dateistruktur

```
ha-log-analyzer/
├── ha_log_analyzer.py    # Script principal / Main script / Hauptskript
├── ha_config.yaml        # Configuration Home Assistant
├── dashboard_card.yaml   # Carte pour le dashboard / Dashboard card
├── hacs.json             # Métadonnées HACS / HACS metadata
├── LICENSE               # Licence MIT
└── README.md             # Ce fichier / This file / Diese Datei
```

## 🔧 Configuration avancée / Advanced Configuration / Erweiterte Konfiguration

### Changer l'heure d'analyse / Change analysis time / Analysezeit ändern

Dans `ha_config.yaml`:
```yaml
trigger:
  - platform: time
    at: "03:00:00"  # 3h du matin / 3:00 AM / 3:00 Uhr
```

### Modifier le nombre de top erreurs / Modify top errors count / Top-Fehler-Anzahl ändern

Dans `ha_log_analyzer.py`, fonction `main()`:
```python
report = generate_report(stats, top_n=20, lang=lang)  # Top 20
```

## 🐛 Dépannage / Troubleshooting / Fehlerbehebung

### Le shell_command ne fonctionne pas
- Vérifiez que vous avez redémarré Home Assistant (pas juste rechargé YAML)
- Vérifiez le chemin: `/config/scripts/ha_log_analyzer.py`

### Erreur "File not found"
- Assurez-vous que le script est exécutable
- Vérifiez les permissions du fichier

### Le sensor reste à 0
- Exécutez manuellement: `Services → shell_command.analyze_ha_logs_fr`
- Vérifiez `/config/log_analysis.json` est créé

## 🤝 Contribution

Les PRs sont les bienvenues! / PRs welcome! / PRs willkommen!

### Idées d'améliorations / Improvement ideas / Verbesserungsideen
- [ ] Graphiques de tendance / Trend graphs / Trendgrafiken
- [ ] Alertes sur nouvelles erreurs critiques / Critical error alerts / Kritische Fehler-Warnungen
- [ ] Comparaison jour/jour / Day-to-day comparison / Tag-zu-Tag-Vergleich
- [ ] Export CSV / PDF
- [ ] Plus de langues / More languages / Mehr Sprachen

## 📄 Licence / License / Lizenz

MIT License - Faites-en ce que vous voulez! / Do whatever you want! / Machen Sie was Sie wollen! 🎉

Voir le fichier [LICENSE](LICENSE) pour les détails.

## 🙏 Crédits / Credits / Danksagungen

- **Auteur / Author / Autor**: th
- **Assistant IA / AI Assistant / KI-Assistent**: Claude (Anthropic) - Conception, développement et documentation / Design, development and documentation / Konzeption, Entwicklung und Dokumentation
- **Communauté / Community / Gemeinschaft**: Home Assistant Community

---

<p align="center">
  Fait avec ❤️ pour la communauté Home Assistant<br>
  Made with ❤️ for the Home Assistant community<br>
  Mit ❤️ für die Home Assistant-Community gemacht
</p>
