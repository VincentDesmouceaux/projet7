"""
Optimisation de la solution en utilisant l'algorithme dynamique du sac à dos (0/1 Knapsack).
"""

import csv
import time
import tracemalloc  # Pour mesurer l'utilisation de la mémoire


def read_actions_from_csv(file_path):
    """
    Lire les données des actions à partir d'un fichier CSV.

    Args:
        file_path (str): Le chemin vers le fichier CSV contenant les données des actions.

    Returns:
        list: Une liste de tuples représentant les actions. Chaque tuple contient (nom de l'action, coût, bénéfice).
    """
    actions = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            actions.append((row['Actions'], int(row['Cost']), float(row['Benefit'])))
    return actions


def knapsack(actions, budget):
    """
    Résoudre le problème du sac à dos en utilisant une approche dynamique.

    Args:
        actions (list): Une liste de tuples représentant les actions. Chaque tuple contient (nom de l'action, coût, bénéfice).
        budget (int): Le budget maximal en euros.

    Returns:
        tuple: La meilleure combinaison d'actions, le coût total et le profit total.
    """
    n = len(actions)

    # Création de la table dp pour stocker les profits maximaux
    dp = [[0 for _ in range(budget + 1)] for _ in range(n + 1)]

    # Remplissage de la table dp
    for i in range(1, n + 1):
        name, cost, benefit = actions[i - 1]
        for w in range(budget + 1):
            if cost <= w:
                # Si l'action peut être ajoutée au budget, on choisit le maximum entre
                # ne pas ajouter l'action ou ajouter l'action et ajouter son bénéfice
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - cost] + cost * (benefit / 100))
            else:
                # Si l'action ne peut pas être ajoutée au budget, on garde le bénéfice sans l'ajouter
                dp[i][w] = dp[i - 1][w]

    # Le profit maximum est trouvé à dp[n][budget]
    max_profit = dp[n][budget]

    # Retraçage des actions sélectionnées pour obtenir le maximum de profit
    w = budget
    best_combination = []

    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            name, cost, benefit = actions[i - 1]
            best_combination.append((name, cost, benefit))
            w -= cost

    # Inversion de la liste pour avoir les actions dans l'ordre original
    best_combination.reverse()

    # Calcul du coût total de la meilleure combinaison
    total_cost = sum(cost for _, cost, _ in best_combination)

    return best_combination, total_cost, max_profit


def main():
    """
    Point d'entrée principal du programme. Lit les données, trouve la meilleure combinaison d'actions, et affiche les résultats.
    """
    start_time = time.time()
    tracemalloc.start()  # Démarrer le suivi de l'utilisation de la mémoire

    # Lire les données des actions depuis le fichier CSV
    actions = read_actions_from_csv('data/actions.csv')

    # Budget maximal
    budget = 500

    # Trouver la meilleure combinaison d'actions
    best_combination, total_cost, max_profit = knapsack(actions, budget)

    # Afficher la meilleure combinaison et le bénéfice correspondant
    print("Meilleure combinaison d'actions pour un budget de 500€:")
    for action in best_combination:
        print(f"{action[0]} - Coût: {action[1]}€ - Bénéfice: {action[2]}%")
    print(f"Coût total de la meilleure combinaison: {total_cost}€")
    print(f"Profit total après 2 ans: {max_profit:.2f}€")

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()  # Obtenir l'utilisation actuelle et maximale de la mémoire
    tracemalloc.stop()

    print(f"Temps d'exécution: {end_time - start_time:.4f} secondes")
    print(f"Utilisation de la mémoire: {current / 10**6:.2f} Mo (actuelle), {peak / 10**6:.2f} Mo (maximum)")


if __name__ == "__main__":
    main()
