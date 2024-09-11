import time


def charger_donnees(chemin_fichier):
    with open(chemin_fichier, 'r') as fichier:
        lignes = fichier.readlines()[1:]  # Ignorer l'en-tête
    actions = []
    for ligne in lignes:
        parties = ligne.strip().split(',')
        if len(parties) < 3:
            print(f"Ligne ignorée, mal formatée : {ligne}")
            continue
        nom_action = parties[0]
        try:
            cout = int(float(parties[1]))
            benefice = float(parties[2])  # Garder le bénéfice en pourcentage
        except ValueError:
            print(f"Erreur de conversion pour la ligne : {ligne}")
            continue
        actions.append((nom_action, cout, benefice))
    return actions


def sac_a_dos(actions, budget_max):
    dp = [[0 for _ in range(budget_max + 1)] for _ in range(len(actions) + 1)]

    for i in range(1, len(actions) + 1):
        nom_action, cout, benefice = actions[i - 1]
        print(f"==> Considération de l'action {nom_action} (Coût : {cout}, Bénéfice : {benefice}%)\n")

        for budget in range(budget_max + 1):
            if cout <= budget:
                sans_action = dp[i - 1][budget]
                avec_action = dp[i - 1][budget - cout] + (benefice * cout / 100)
                dp[i][budget] = max(sans_action, avec_action)
            else:
                dp[i][budget] = dp[i - 1][budget]

        print(f"\nTable DP après la considération de l'action {nom_action}:")
        for ligne in dp:
            print(' '.join([f"{val:5.2f}" for val in ligne]))
        print("\n")
        time.sleep(0.5)

    print("==> Retour en arrière pour déterminer l'ensemble optimal d'actions :")
    budget = budget_max
    actions_choisies = []
    for i in range(len(actions), 0, -1):
        if dp[i][budget] != dp[i - 1][budget]:
            nom_action, cout, benefice = actions[i - 1]
            actions_choisies.append((nom_action, cout, benefice))
            budget -= cout
            print(f"  Action choisie : {nom_action} (Coût : {
                  cout}, Bénéfice : {benefice}%). Budget restant : {budget}")
        else:
            print(f"  Action {actions[i - 1][0]} ignorée (aucun impact sur le meilleur profit actuel).")

    actions_choisies.reverse()  # Remettre dans l'ordre initial

    print("\n==> Meilleure combinaison d'actions pour un budget de 500€:")
    total_cost = 0
    total_profit = 0
    for action in actions_choisies:
        nom_action, cout, benefice = action
        total_cost += cout
        total_profit += cout * benefice / 100
        print(f"{nom_action} - Coût: {cout}€ - Bénéfice: {benefice}%")

    print(f"Coût total de la meilleure combinaison: {total_cost}€")
    print(f"Profit total après 2 ans: {total_profit:.2f}€")


if __name__ == "__main__":
    chemin_fichier = "data/actions.csv"  # Remplacer par le chemin de votre fichier
    actions = charger_donnees(chemin_fichier)
    budget_max = 500
    sac_a_dos(actions, budget_max)
