"""
TP4 — Profiling cProfile · API GameStore
=========================================
Objectif : identifier et corriger le bottleneck dans /games/stats

Étapes :
  1. Lancer le profiler sur l'endpoint /games/stats
  2. Analyser la sortie : trouver la fonction avec le cumtime le plus élevé
  3. Corriger la fonction _calculate_stats() dans app_gamestore.py
  4. Re-profiler et comparer avant/après

Lancement du profiler :
  python -m cProfile -s cumulative profile_tp4.py
  python -m cProfile -o profile.out profile_tp4.py && snakeviz profile.out
"""

import cProfile
import pstats
import io
import sys
import os
import time

# Ajouter le dossier parent au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app_gamestore import app, init_db

# ── Utilitaire de mesure ──────────────────────────────────────────────────────

def profile_endpoint(url, n_calls=50):
    """
    Profile n_calls appels à un endpoint Flask et retourne les stats.
    """
    with app.test_client() as client:
        with app.app_context():
            init_db()

        pr = cProfile.Profile()
        pr.enable()

        for _ in range(n_calls):
            client.get(url)

        pr.disable()

    stream = io.StringIO()
    stats  = pstats.Stats(pr, stream=stream)
    stats.sort_stats('cumulative')
    stats.print_stats(15)
    return stream.getvalue(), pr


# ── Exercice principal ────────────────────────────────────────────────────────

if __name__ == '__main__':
    print('=' * 65)
    print('TP4 — Profiling cProfile sur /games/stats')
    print('=' * 65)

    print('\n>>> Profiling de /games/stats (50 appels)...\n')
    output, pr = profile_endpoint('/games/stats', n_calls=50)
    print(output)

    print('\n>>> Mesure du temps moyen de réponse...')
    with app.test_client() as client:
        with app.app_context():
            init_db()
        times = []
        for _ in range(20):
            start = time.perf_counter()
            client.get('/games/stats')
            times.append((time.perf_counter() - start) * 1000)

    avg = sum(times) / len(times)
    print(f'    Temps moyen : {avg:.1f} ms')
    print(f'    Min : {min(times):.1f} ms  |  Max : {max(times):.1f} ms')

    print('\n>>> Questions à répondre :')
    print('    1. Quelle fonction a le cumtime le plus élevé ?')
    print('    2. Pourquoi est-elle lente ? (regarder le ncalls)')
    print('    3. Comment la corriger pour atteindre < 5ms ?')
    print()

    # Sauvegarder pour snakeviz
    pr.dump_stats('profile.out')
    print('>>> Profil sauvegardé dans profile.out')
    print('    Visualiser : snakeviz profile.out')
