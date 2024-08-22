import csv
import time
import tracemalloc  # Pour mesurer l'utilisation de la mémoire


def read_actions_from_csv(file_path):
    """
    Lit un fichier CSV contenant des actions et retourne une liste de tuples
    contenant le nom de l'action, son coût et son bénéfice.

    Args:
        file_path (str): Le chemin vers le fichier CSV.

    Returns:
        list of tuple: Une liste de tuples contenant le nom, le coût et le bénéfice de chaque action.
    """
    actions = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            actions.append((row['Actions'], int(row['Cost']), float(row['Benefit'])))
    return actions


def calculate_profit(actions):
    """
    Calcule le profit total pour une combinaison donnée d'actions.

    Args:
        actions (list of tuple): Une liste de tuples représentant une combinaison d'actions.

    Returns:
        float: Le profit total pour la combinaison donnée.
    """
    return sum(cost * (profit / 100) for _, cost, profit in actions)


def generate_combinations(actions):
    """
    Génère toutes les combinaisons possibles d'une liste d'actions.

    Args:
        actions (list of tuple): La liste des actions.

    Returns:
        list of list of tuple: Une liste de combinaisons, chaque combinaison étant une liste d'actions.
    """
    combinations = []
    n = len(actions)
    for i in range(1, 2 ** n):
        combination = []
        for j in range(n):
            if i & (1 << j):
                combination.append(actions[j])
        combinations.append(combination)
    return combinations


def find_best_investment(actions, budget):
    """
    Trouve la meilleure combinaison d'investissement pour un budget donné en maximisant le profit.

    Args:
        actions (list of tuple): La liste des actions sous forme de tuples (nom, coût, bénéfice).
        budget (int): Le budget maximal.

    Returns:
        tuple: La meilleure combinaison d'actions, le profit maximal et le coût total de la combinaison.
    """
    best_combination = []
    max_profit = 0
    min_cost = float('inf')

    all_combinations = generate_combinations(actions)

    for combination in all_combinations:
        total_cost = sum(cost for _, cost, _ in combination)
        if total_cost <= budget:
            profit = calculate_profit(combination)
            if profit > max_profit or (profit == max_profit and total_cost < min_cost):
                max_profit = profit
                best_combination = combination
                min_cost = total_cost

    return best_combination, max_profit, min_cost


def main():
    """
    Point d'entrée principal du programme. Lit les actions à partir d'un fichier CSV,
    trouve la meilleure combinaison d'investissement pour un budget donné,
    et affiche les résultats, y compris le coût total, le profit total,
    le temps d'exécution et l'utilisation de la mémoire.
    """
    start_time = time.time()
    tracemalloc.start()  # Démarrer le suivi de l'utilisation de la mémoire

    actions = read_actions_from_csv('data/actions.csv')
    budget = 500

    best_combination, max_profit, min_cost = find_best_investment(actions, budget)

    print("\nMeilleure combinaison d'actions pour un budget de 500€:")
    for action in best_combination:
        print(f"{action[0]} - Coût: {action[1]}€ - Bénéfice: {action[2]}%")
    print(f"Coût total de la meilleure combinaison: {min_cost}€")
    print(f"Profit total après 2 ans: {max_profit:.2f}€")

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()  # Obtenir l'utilisation actuelle et maximale de la mémoire
    tracemalloc.stop()

    print(f"Temps d'exécution: {end_time - start_time:.4f} secondes")
    print(f"Utilisation de la mémoire: {current / 10**6:.2f} Mo (actuelle), {peak / 10**6:.2f} Mo (maximum)")


if __name__ == "__main__":
    main()
