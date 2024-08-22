import csv
import time
import tracemalloc  # Pour mesurer l'utilisation de la mémoire


def read_actions_from_csv(file_path):
    actions = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            actions.append((row['Actions'], int(row['Cost']), float(row['Benefit'])))
    return actions


def knapsack(actions, max_budget):
    total_actions = len(actions)
    profit_table = [[0 for _ in range(max_budget + 1)] for _ in range(total_actions + 1)]

    for action_index in range(1, total_actions + 1):
        action_name, action_cost, action_benefit = actions[action_index - 1]
        for current_budget in range(max_budget + 1):
            if action_cost <= current_budget:
                profit_table[action_index][current_budget] = max(
                    profit_table[action_index - 1][current_budget],
                    profit_table[action_index - 1][current_budget - action_cost] + action_cost * (action_benefit / 100)
                )
            else:
                profit_table[action_index][current_budget] = profit_table[action_index - 1][current_budget]

    max_profit = profit_table[total_actions][max_budget]
    remaining_budget = max_budget
    best_combination = []

    for action_index in range(total_actions, 0, -1):
        if profit_table[action_index][remaining_budget] != profit_table[action_index - 1][remaining_budget]:
            action_name, action_cost, action_benefit = actions[action_index - 1]
            best_combination.append((action_name, action_cost, action_benefit))
            remaining_budget -= action_cost

    best_combination.reverse()
    total_cost = sum(action_cost for _, action_cost, _ in best_combination)

    return best_combination, total_cost, max_profit


def main():
    start_time = time.time()
    tracemalloc.start()  # Démarrer le suivi de l'utilisation de la mémoire

    actions = read_actions_from_csv('data/actions.csv')
    max_budget = 500

    best_combination, total_cost, max_profit = knapsack(actions, max_budget)

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
