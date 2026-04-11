# WARNING: Diese Datei enthält bewusst unsichere Code-Patterns
# ausschließlich zum Testen der Bandit CI-Integration.
# Niemals in Production verwenden.

#import hashlib
#import pickle
#import subprocess
#import xml.etree.ElementTree as ET

# ── B324 – Schwacher Hash-Algorithmus ─────────────────────────────────────────
# MD5 und SHA1 sind kollisionsanfällig, nicht für Sicherheitszwecke geeignet
#weak_hash = hashlib.md5(b"passwort123").hexdigest()
#also_weak = hashlib.sha1(b"geheim").hexdigest()

# ── B602 – Shell Injection ─────────────────────────────────────────────────────
# shell=True übergibt den String direkt an die Shell – gefährlich mit User-Input
#user_input = "foo; rm -rf /"
#subprocess.call(user_input, shell=True)

# ── B301 / B403 – Unsicheres Deserialisieren ───────────────────────────────────
# pickle kann beliebigen Code ausführen beim Deserialisieren
#data = b"\x80\x04\x95..."
#obj = pickle.loads(data)

# ── B105 – Hardcoded Password ──────────────────────────────────────────────────
# Credentials im Source Code sind ein klassischer Supply-Chain-Angriffsvektor
#password = "supersecret123"
#api_key = "AKIAIOSFODNN7EXAMPLE"

# ── B320 / B410 – XML External Entity (XXE) ───────────────────────────────────
# ElementTree in älteren Python-Versionen anfällig für XXE-Angriffe
#tree = ET.parse("user_data.xml")

# ── B101 – Assert für Sicherheitschecks ───────────────────────────────────────
# assert-Statements werden bei python -O (optimized) komplett wegkompiliert
#def check_admin(user):
#    assert user.is_admin, "Kein Zugriff"
#    return True