#!/usr/bin/env python3
"""
Home Assistant Log Analyzer
Analyse les logs HA et génère un rapport statistique des erreurs.

Usage:
    python ha_log_analyzer.py [chemin_vers_log] [langue]
    
Par défaut: /config/home-assistant.log, langue: fr
Langues supportées: fr, en, de
"""

import re
import sys
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

# ============================================
# TRADUCTIONS
# ============================================
TRANSLATIONS = {
    'fr': {
        'analyzing': '🔍 Analyse de',
        'report_title': '📊 HOME ASSISTANT LOG ANALYZER - RAPPORT',
        'generated_on': 'Généré le',
        'total_entries': 'Entrées totales analysées',
        'filtered_entries': 'Entrées filtrées',
        'summary_by_severity': '📈 RÉSUMÉ PAR SÉVÉRITÉ',
        'by_integration': '📦 PAR INTÉGRATION',
        'top_errors': '🔝 TOP {n} ERREURS PAR FRÉQUENCE',
        'first': 'Première',
        'last': 'Dernière',
        'end_report': 'Fin du rapport',
        'file_not_found': '❌ Fichier non trouvé',
        'json_saved': '💾 Rapport JSON sauvegardé',
        'errors': 'erreurs',
        'files': 'fichiers',
    },
    'en': {
        'analyzing': '🔍 Analyzing',
        'report_title': '📊 HOME ASSISTANT LOG ANALYZER - REPORT',
        'generated_on': 'Generated on',
        'total_entries': 'Total entries analyzed',
        'filtered_entries': 'Filtered entries',
        'summary_by_severity': '📈 SUMMARY BY SEVERITY',
        'by_integration': '📦 BY INTEGRATION',
        'top_errors': '🔝 TOP {n} ERRORS BY FREQUENCY',
        'first': 'First',
        'last': 'Last',
        'end_report': 'End of report',
        'file_not_found': '❌ File not found',
        'json_saved': '💾 JSON report saved',
        'errors': 'errors',
        'files': 'files',
    },
    'de': {
        'analyzing': '🔍 Analyse von',
        'report_title': '📊 HOME ASSISTANT LOG ANALYZER - BERICHT',
        'generated_on': 'Erstellt am',
        'total_entries': 'Gesamteinträge analysiert',
        'filtered_entries': 'Gefilterte Einträge',
        'summary_by_severity': '📈 ZUSAMMENFASSUNG NACH SCHWEREGRAD',
        'by_integration': '📦 NACH INTEGRATION',
        'top_errors': '🔝 TOP {n} FEHLER NACH HÄUFIGKEIT',
        'first': 'Erste',
        'last': 'Letzte',
        'end_report': 'Ende des Berichts',
        'file_not_found': '❌ Datei nicht gefunden',
        'json_saved': '💾 JSON-Bericht gespeichert',
        'errors': 'Fehler',
        'files': 'Dateien',
    }
}

def get_text(key: str, lang: str = 'fr', **kwargs) -> str:
    """Récupère le texte traduit."""
    text = TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)
    return text.format(**kwargs) if kwargs else text


# ============================================
# PARSING
# ============================================
LOG_PATTERN = re.compile(
    r'^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+)\s+'
    r'(?P<severity>DEBUG|INFO|WARNING|ERROR|CRITICAL)\s+'
    r'\((?P<thread>[^)]+)\)\s+'
    r'\[(?P<source>[^\]]+)\]\s+'
    r'(?P<message>.*)$'
)

INTEGRATION_PATTERN = re.compile(r'^(?:homeassistant\.)?(?:components\.)?([^\.]+)')


def parse_log_file(log_path: str) -> list[dict]:
    """Parse le fichier de log et retourne une liste d'entrées."""
    entries = []
    current_entry = None
    
    with open(log_path, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            match = LOG_PATTERN.match(line.strip())
            if match:
                if current_entry:
                    entries.append(current_entry)
                current_entry = {
                    'timestamp': match.group('timestamp'),
                    'severity': match.group('severity'),
                    'thread': match.group('thread'),
                    'source': match.group('source'),
                    'message': match.group('message'),
                    'traceback': []
                }
            elif current_entry and line.strip():
                current_entry['traceback'].append(line.rstrip())
    
    if current_entry:
        entries.append(current_entry)
    
    return entries


def extract_integration(source: str) -> str:
    """Extrait le nom de l'intégration depuis la source."""
    match = INTEGRATION_PATTERN.match(source)
    if match:
        return match.group(1)
    return source.split('.')[0] if '.' in source else source


def normalize_message(message: str) -> str:
    """Normalise un message pour regrouper les erreurs similaires."""
    message = re.sub(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', '<UUID>', message, flags=re.I)
    message = re.sub(r'(sensor|switch|light|binary_sensor|automation|script|input_\w+)\.[a-z0-9_]+', r'\1.<entity>', message, flags=re.I)
    message = re.sub(r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}', '<TIMESTAMP>', message)
    message = re.sub(r'\b\d{4,}\b', '<NUM>', message)
    message = re.sub(r'https?://[^\s]+', '<URL>', message)
    message = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '<IP>', message)
    if len(message) > 150:
        message = message[:147] + '...'
    return message


# ============================================
# ANALYSE
# ============================================
def analyze_logs(entries: list[dict], severities: list[str] = None) -> dict:
    """Analyse les entrées et génère les statistiques."""
    if severities is None:
        severities = ['ERROR', 'WARNING', 'CRITICAL']
    
    filtered = [e for e in entries if e['severity'] in severities]
    
    stats = {
        'total_entries': len(entries),
        'filtered_entries': len(filtered),
        'severities_filter': severities,
        'by_severity': defaultdict(int),
        'by_integration': defaultdict(lambda: defaultdict(int)),
        'top_errors': defaultdict(int),
        'first_occurrence': {},
        'last_occurrence': {},
    }
    
    for entry in filtered:
        severity = entry['severity']
        integration = extract_integration(entry['source'])
        normalized_msg = normalize_message(entry['message'])
        error_key = f"{integration}|{severity}|{normalized_msg}"
        
        stats['by_severity'][severity] += 1
        stats['by_integration'][integration][severity] += 1
        stats['top_errors'][error_key] += 1
        
        if error_key not in stats['first_occurrence']:
            stats['first_occurrence'][error_key] = entry['timestamp']
        stats['last_occurrence'][error_key] = entry['timestamp']
    
    return stats


# ============================================
# RAPPORTS
# ============================================
def generate_report(stats: dict, top_n: int = 10, lang: str = 'fr') -> str:
    """Génère un rapport formaté."""
    lines = []
    lines.append("=" * 70)
    lines.append(get_text('report_title', lang))
    lines.append("=" * 70)
    lines.append(f"{get_text('generated_on', lang)}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"{get_text('total_entries', lang)}: {stats['total_entries']}")
    lines.append(f"{get_text('filtered_entries', lang)} ({', '.join(stats['severities_filter'])}): {stats['filtered_entries']}")
    lines.append("")
    
    # Par sévérité
    lines.append("-" * 70)
    lines.append(get_text('summary_by_severity', lang))
    lines.append("-" * 70)
    for severity in ['CRITICAL', 'ERROR', 'WARNING']:
        count = stats['by_severity'].get(severity, 0)
        if count > 0:
            icon = {'CRITICAL': '🔴', 'ERROR': '🟠', 'WARNING': '🟡'}.get(severity, '⚪')
            lines.append(f"  {icon} {severity}: {count}")
    lines.append("")
    
    # Par intégration
    lines.append("-" * 70)
    lines.append(get_text('by_integration', lang))
    lines.append("-" * 70)
    
    integrations_sorted = sorted(
        stats['by_integration'].items(),
        key=lambda x: sum(x[1].values()),
        reverse=True
    )
    
    for integration, severities in integrations_sorted[:15]:
        total = sum(severities.values())
        details = ', '.join(f"{s}: {c}" for s, c in sorted(severities.items()) if c > 0)
        lines.append(f"  {integration}: {total} ({details})")
    lines.append("")
    
    # Top erreurs
    lines.append("-" * 70)
    lines.append(get_text('top_errors', lang, n=top_n))
    lines.append("-" * 70)
    
    top_errors = sorted(stats['top_errors'].items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    for i, (error_key, count) in enumerate(top_errors, 1):
        integration, severity, message = error_key.split('|', 2)
        first = stats['first_occurrence'].get(error_key, 'N/A')
        last = stats['last_occurrence'].get(error_key, 'N/A')
        
        icon = {'CRITICAL': '🔴', 'ERROR': '🟠', 'WARNING': '🟡'}.get(severity, '⚪')
        lines.append(f"\n  {i}. {icon} [{integration}] x{count}")
        lines.append(f"     {message}")
        lines.append(f"     {get_text('first', lang)}: {first[:19]} | {get_text('last', lang)}: {last[:19]}")
    
    lines.append("")
    lines.append("=" * 70)
    lines.append(get_text('end_report', lang))
    lines.append("=" * 70)
    
    return '\n'.join(lines)


def generate_json_report(stats: dict, top_n: int = 10, lang: str = 'fr') -> dict:
    """Génère un rapport au format JSON."""
    top_errors = sorted(stats['top_errors'].items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    top_errors_list = []
    for error_key, count in top_errors:
        integration, severity, message = error_key.split('|', 2)
        top_errors_list.append({
            'integration': integration,
            'severity': severity,
            'message': message,
            'count': count,
            'first_occurrence': stats['first_occurrence'].get(error_key),
            'last_occurrence': stats['last_occurrence'].get(error_key),
        })
    
    return {
        'timestamp': datetime.now().isoformat(),
        'language': lang,
        'total_entries': stats['total_entries'],
        'filtered_entries': stats['filtered_entries'],
        'by_severity': dict(stats['by_severity']),
        'by_integration': {k: dict(v) for k, v in stats['by_integration'].items()},
        'top_errors': top_errors_list,
    }


# ============================================
# MAIN
# ============================================
def main():
    # Arguments: [log_path] [lang]
    log_path = sys.argv[1] if len(sys.argv) > 1 else '/config/home-assistant.log'
    lang = sys.argv[2] if len(sys.argv) > 2 else 'fr'
    
    if lang not in TRANSLATIONS:
        lang = 'en'
    
    if not Path(log_path).exists():
        print(f"{get_text('file_not_found', lang)}: {log_path}")
        sys.exit(1)
    
    print(f"{get_text('analyzing', lang)} {log_path}...")
    
    entries = parse_log_file(log_path)
    stats = analyze_logs(entries, severities=['ERROR', 'WARNING', 'CRITICAL'])
    
    report = generate_report(stats, top_n=10, lang=lang)
    json_report = generate_json_report(stats, top_n=10, lang=lang)
    
    print(report)
    
    json_path = Path(log_path).parent / 'log_analysis.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_report, f, indent=2, ensure_ascii=False)
    print(f"\n{get_text('json_saved', lang)}: {json_path}")


if __name__ == '__main__':
    main()
