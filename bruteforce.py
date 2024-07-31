"""
Plan de développement:
1. Lire les données des actions à partir d'un fichier.
2. Générer toutes les combinaisons possibles d'actions.
3. Filtrer les combinaisons qui respectent le budget de 500 euros.
4. Calculer les bénéfices pour chaque combinaison valide.
5. Sélectionner la combinaison avec le bénéfice maximal et le coût total le plus bas.
"""

import csv
import time  # Importation du module time pour mesurer le temps d'exécution


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
        reader = csv.DictReader(file)  # Utilisation de DictReader pour lire le CSV en tant que dictionnaire
        for row in reader:
            # Ajout de chaque ligne comme un tuple
            actions.append((row['Actions'], int(row['Cost']), float(row['Benefit'])))
    return actions


def calculate_profit(actions):
    """
    Calculer le bénéfice total pour une combinaison d'actions.

    Args:
        actions (list): Une liste de tuples représentant les actions. Chaque tuple contient (nom de l'action, coût, bénéfice).

    Returns:
        float: Le bénéfice total pour la combinaison d'actions.
    """
    return sum(cost * (profit / 100) for _, cost, profit in actions)  # Calcul du bénéfice total en pourcentage du coût


def generate_combinations(actions):
    """
    Complexité temporelle  O(2**n)

    - La génération de toutes les combinaisons possibles dans generate_combinations.

    Complexité spatiale O(2**n)

    - Le stockage de toutes les combinaisons possibles dans la liste combinations dans generate_combinations.

    Générer toutes les combinaisons possibles d'actions.

    Args:
        actions (list): Une liste de tuples représentant les actions.

    Returns:
        list: Une liste de toutes les combinaisons possibles d'actions.
    """
    combinations = []
    n = len(actions)

    # Utiliser une boucle pour générer toutes les combinaisons possibles
    for i in range(1, 2 ** n):
        combination = []
        for j in range(n):
            if i & (1 << j):  # Utilisation de la manipulation de bits pour générer les combinaisons
                combination.append(actions[j])
        combinations.append(combination)

    return combinations


def find_best_investment(actions, budget):
    """
    Complexité temporelle  O(2**n)

    - La boucle sur toutes les combinaisons générées et l'évaluation de chaque combinaison dans find_best_investment.

    Trouver la meilleure combinaison d'actions qui maximise le bénéfice tout en respectant le budget,
    puis parmi celles-ci, sélectionner celle dont le coût total est le plus bas possible.

    Args:
        actions (list): Une liste de tuples représentant les actions. Chaque tuple contient (nom de l'action, coût, bénéfice).
        budget (int): Le budget maximal en euros.

    Returns:
        tuple: La meilleure combinaison d'actions en termes de bénéfice et le bénéfice total.
    """
    best_combination = []
    max_profit = 0
    min_cost = float('inf')  # Initialisation du coût minimum avec une valeur infinie

    all_combinations = generate_combinations(actions)  # Génération de toutes les combinaisons possibles

    for combination in all_combinations:
        total_cost = sum(cost for _, cost, _ in combination)  # Calcul du coût total de la combinaison
        if total_cost <= budget:  # Vérification si la combinaison respecte le budget
            profit = calculate_profit(combination)  # Calcul du bénéfice total de la combinaison
            if profit > max_profit or (profit == max_profit and total_cost < min_cost):
                # Mise à jour de la meilleure combinaison si le bénéfice est supérieur ou si le bénéfice est égal mais le coût est inférieur
                max_profit = profit
                best_combination = combination
                min_cost = total_cost

    return best_combination, max_profit, min_cost  # Retourne la meilleure combinaison trouvée, le profit et le coût


def main():
    """
    Point d'entrée principal du programme. Lit les données, trouve la meilleure combinaison d'actions, et affiche les résultats.
    """
    start_time = time.time()  # Capture le temps de début pour mesurer la durée de l'exécution

    # Lire les données des actions depuis le fichier CSV
    actions = read_actions_from_csv('data/actions.csv')

    # Budget maximal
    budget = 500

    # Trouver la meilleure combinaison d'actions
    best_combination, max_profit, min_cost = find_best_investment(actions, budget)

    # Afficher la meilleure combinaison et le bénéfice correspondant
    print("Meilleure combinaison d'actions pour un budget de 500€:")
    for action in best_combination:
        print(f"{action[0]} - Coût: {action[1]}€ - Bénéfice: {action[2]}%")
    print(f"Coût total de la meilleure combinaison: {min_cost}€")
    print(f"Profit total après 2 ans: {max_profit:.2f}€")

    end_time = time.time()  # Capture le temps de fin
    print(f"Temps d'exécution: {end_time - start_time:.4f} secondes")  # Affiche le temps d'exécution


if __name__ == "__main__":
    main()  # Appelle la fonction main si ce fichier est exécuté en tant que script
