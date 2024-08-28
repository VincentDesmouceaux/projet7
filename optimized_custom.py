import csv
import time
import tracemalloc  # Pour mesurer l'utilisation de la mémoire


def read_actions_from_csv(file_path):
    """
    Lit les données d'un fichier CSV et les retourne sous forme de liste de tuples.

    Chaque tuple contient le nom de l'action, son coût (converti en centimes) et son pourcentage de profit.

    Args:
        file_path (str): Le chemin vers le fichier CSV à lire.

    Returns:
        list of tuple: Une liste de tuples, où chaque tuple contient (nom de l'action, coût en centimes, pourcentage de profit).
    """
    actions = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                name = row['name']
                price = float(row['price']) * 100  # Convertir en centimes
                profit = float(row['profit'])

                # Ignorer les actions avec des prix ou profits négatifs ou nuls
                if price > 0 and profit > 0:
                    actions.append((name, price, profit))
            except ValueError as e:
                continue
    return actions


def knapsack(actions, max_budget):
    """
    Implémente l'algorithme du sac à dos pour sélectionner les actions qui maximisent le profit sans dépasser le budget.

    Args:
        actions (list of tuple): Une liste de tuples représentant les actions, où chaque tuple contient (nom de l'action, coût en centimes, pourcentage de profit).
        max_budget (int): Le budget maximal en euros.

    Returns:
        tuple: Contient la meilleure combinaison d'actions (list of tuple), le coût total en euros (float), et le profit total en euros (float).
    """
    max_budget = int(max_budget * 100)  # Convertir le budget en centimes
    total_actions = len(actions)
    profit_table = [[0 for _ in range(max_budget + 1)] for _ in range(total_actions + 1)]

    for action_index in range(1, total_actions + 1):
        action_name, action_cost, action_benefit = actions[action_index - 1]
        for current_budget in range(max_budget + 1):
            if action_cost <= current_budget:
                profit_table[action_index][current_budget] = max(
                    profit_table[action_index - 1][current_budget],
                    profit_table[action_index - 1][current_budget -
                                                   int(action_cost)] + action_cost * (action_benefit / 100)
                )
            else:
                profit_table[action_index][current_budget] = profit_table[action_index - 1][current_budget]

    max_profit = profit_table[total_actions][max_budget] / 100  # Reconvertir le profit en euros
    remaining_budget = max_budget
    best_combination = []

    for action_index in range(total_actions, 0, -1):
        if profit_table[action_index][remaining_budget] != profit_table[action_index - 1][remaining_budget]:
            action_name, action_cost, action_benefit = actions[action_index - 1]
            best_combination.append((action_name, action_cost, action_benefit))
            remaining_budget -= int(action_cost)

    best_combination.reverse()
    total_cost = sum(action_cost for _, action_cost, _ in best_combination)

    # Remarque : `total_cost` est en centimes ici et est converti en euros lors de son retour
    return best_combination, total_cost / 100, max_profit  # Reconvertir total_cost en euros


def execute_and_compare(file_path, max_budget, sienna_total_cost, sienna_total_return):
    """
    Exécute l'algorithme du sac à dos sur un ensemble de données et compare les résultats avec ceux de Sienna.

    Args:
        file_path (str): Le chemin vers le fichier CSV contenant les données d'actions.
        max_budget (int): Le budget maximal en euros.
        sienna_total_cost (float): Le coût total de la sélection de Sienna en euros.
        sienna_total_return (float): Le retour total de la sélection de Sienna en euros.
    """
    start_time = time.time()
    tracemalloc.start()

    actions = read_actions_from_csv(file_path)
    best_combination, total_cost, max_profit = knapsack(actions, max_budget)

    if not best_combination:
        print(f"\nAucune combinaison valide pour {file_path} dans le budget de {max_budget}€.")
        return

    print(f"\nRésultats pour {file_path}:")
    print("Meilleure combinaison d'actions:")
    for action in best_combination:
        print(f"{action[0]} - Coût: {action[1] / 100:.2f}€ - Bénéfice: {action[2]:.2f}%")
    print(f"\nCoût total de la meilleure combinaison: {total_cost:.2f}€")
    print(f"Profit total après 2 ans: {max_profit:.2f}€")

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"\nTemps d'exécution: {end_time - start_time:.4f} secondes")
    print(f"Utilisation de la mémoire: {current / 10**6:.2f} Mo (actuelle), {peak / 10**6:.2f} Mo (maximum)")

    print("\nComparaison avec Sienna:")
    cost_difference = total_cost - sienna_total_cost
    profit_difference = max_profit - sienna_total_return

    print(f"Coût total Sienna: {sienna_total_cost:.2f}€")
    print(f"Retour total Sienna: {sienna_total_return:.2f}€")
    print(f"Différence de coût (votre combinaison - Sienna): {cost_difference:.2f}€")
    print(f"Différence de profit (votre combinaison - Sienna): {profit_difference:.2f}€")

    if cost_difference > 0:
        print(f"Votre combinaison coûte {cost_difference:.2f}€ de plus que celle de Sienna.")
    else:
        print(f"Votre combinaison coûte {-cost_difference:.2f}€ de moins que celle de Sienna.")

    if profit_difference > 0:
        print(f"Votre combinaison rapporte {profit_difference:.2f}€ de plus que celle de Sienna.")
    else:
        print(f"Votre combinaison rapporte {-profit_difference:.2f}€ de moins que celle de Sienna.")


if __name__ == "__main__":
    execute_and_compare('data/dataset1_Python+P7.csv', 500, 498.76, 196.61)
    execute_and_compare('data/dataset2_Python+P7.csv', 500, 489.24, 193.78)
