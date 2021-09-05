doc = {
    "name": "91.",                          # name of the team
    "auth": "12345",                        # auth code
    "superusers": ["Fastlane82", "Samu"],   # users with permission to write to data base
    "games": 13,                            # number of games played
    "history": ["38.", "46."],              # list of past opponents
    "score": 534,                           # current HeLO score
    "checksum": "random",                   # random number for a check sum
    "previous_score": 513                   # old score, before the last game
}

"""
bei falscher Eintragung muss Folgendes gemacht werden:
- alten Score einsetzen
- history letzten Eintrag löschen
- games um 1 reduzieren
"""
