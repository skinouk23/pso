import random
import math

def calcule_distance_totale(solution, matrice_distances):
    distance_totale = 0
    for i in range(len(solution) - 1):
        distance_totale += matrice_distances[solution[i]][solution[i + 1]]
    distance_totale += matrice_distances[solution[-1]][solution[0]]
    return distance_totale

def generer_voisin(solution):
    """Génère un voisin aléatoire en échangeant deux villes"""
    voisin = solution[:]
    i, j = random.sample(range(len(solution)), 2)
    voisin[i], voisin[j] = voisin[j], voisin[i]
    return voisin

def generer_population_initial(taille_population, nombre_villes):
    """Génère une population initiale de solutions aléatoires"""
    population = []
    for _ in range(taille_population):
        solution = list(range(nombre_villes))
        random.shuffle(solution)
        population.append(solution)
    return population

def evaluer_et_trier_population(population, matrice_distances):
    """Évalue et trie la population par distance (croissante)"""
    solutions_avec_distances = []
    for solution in population:
        distance = calcule_distance_totale(solution, matrice_distances)
        solutions_avec_distances.append((solution, distance))
    
    # Trier par distance (meilleures en premier)
    solutions_avec_distances.sort(key=lambda x: x[1])
    
    solutions_triees = [sol for sol, dist in solutions_avec_distances]
    distances_triees = [dist for sol, dist in solutions_avec_distances]
    
    return solutions_triees, distances_triees

def calculer_fitness_par_rang(taille_population, pression_selection=1.5):
    """
    Calcule les fitness basées sur le rang
    Formule: fitness(i) = 2 - pression_selection + 2*(pression_selection - 1)*(i-1)/(taille_population-1)
    """
    fitness = []
    for rang in range(taille_population):
        # Le rang 0 (meilleur) a la fitness la plus élevée
        valeur_fitness = 2 - pression_selection + 2 * (pression_selection - 1) * (taille_population - rang - 1) / (taille_population - 1)
        fitness.append(valeur_fitness)
    return fitness

def selection_rang(population_triee, fitness_rang):
    """Sélectionne une solution selon la méthode par rang"""
    fitness_totale = sum(fitness_rang)
    valeur_aleatoire = random.uniform(0, fitness_totale)
    
    somme_cumulee = 0
    for i in range(len(population_triee)):
        somme_cumulee += fitness_rang[i]
        if somme_cumulee >= valeur_aleatoire:
            return population_triee[i][:]  # Retourne une copie
    
    return population_triee[-1][:]

def algorithme_genetique_rang(matrice_distances, taille_population, nombre_generations, taux_mutation, pression_selection=1.5):
    nombre_villes = len(matrice_distances)
    
    # Initialisation de la population
    population = generer_population_initial(taille_population, nombre_villes)
    
    meilleure_solution = None
    meilleure_distance = float('inf')
    
    # Pré-calcul des fitness par rang
    fitness_rang = calculer_fitness_par_rang(taille_population, pression_selection)
    
    for generation in range(nombre_generations):
        # Évaluation et tri de la population
        population_triee, distances_triees = evaluer_et_trier_population(population, matrice_distances)
        
        # Mise à jour de la meilleure solution
        if distances_triees[0] < meilleure_distance:
            meilleure_solution = population_triee[0][:]
            meilleure_distance = distances_triees[0]
        
        # Création d'une nouvelle population par sélection par rang
        nouvelle_population = []
        
        # Élitisme : conserver les 2 meilleures solutions
        nouvelle_population.append(population_triee[0][:])
        nouvelle_population.append(population_triee[1][:])
        
        # Remplir le reste de la population par sélection par rang et mutation
        while len(nouvelle_population) < taille_population:
            # Sélection par rang de deux parents
            parent1 = selection_rang(population_triee, fitness_rang)
            parent2 = selection_rang(population_triee, fitness_rang)
            
            # Croisement (crossover) - Order Crossover (OX)
            enfant = croisement_ox(parent1, parent2)
            
            # Mutation
            if random.random() < taux_mutation:
                enfant = generer_voisin(enfant)
            
            nouvelle_population.append(enfant)
        
        population = nouvelle_population
        
        # Affichage de progression
        if generation % 100 == 0:
            print(f"Génération {generation}: Meilleure distance = {meilleure_distance}")
    
    return meilleure_solution, meilleure_distance

def croisement_ox(parent1, parent2):
    """Order Crossover (OX) pour le problème TSP"""
    taille = len(parent1)
    point1 = random.randint(0, taille - 2)
    point2 = random.randint(point1 + 1, taille - 1)
    
    enfant = [-1] * taille
    
    # Copier le segment entre point1 et point2 du parent1
    for i in range(point1, point2 + 1):
        enfant[i] = parent1[i]
    
    # Remplir le reste avec les éléments du parent2 dans l'ordre
    position = (point2 + 1) % taille
    for i in range(taille):
        element = parent2[(point2 + 1 + i) % taille]
        if element not in enfant:
            enfant[position] = element
            position = (position + 1) % taille
    
    return enfant

def simulated_annealing_avec_rang(matrice_distances, temperature_initiale, temperature_finale, 
                                taux_refroidissement, iterations_par_temperature, taille_population_rang):
    """Version hybride avec sélection par rang pour générer les voisins"""
    
    nombre_villes = len(matrice_distances)
    
    # Solution initiale aléatoire
    solution_actuelle = list(range(nombre_villes))
    random.shuffle(solution_actuelle)
    distance_actuelle = calcule_distance_totale(solution_actuelle, matrice_distances)
    
    meilleure_solution = solution_actuelle[:]
    meilleure_distance = distance_actuelle
    
    temperature = temperature_initiale
    
    # Pré-calcul des fitness par rang
    fitness_rang = calculer_fitness_par_rang(taille_population_rang, pression_selection=1.5)
    
    while temperature > temperature_finale:
        # Générer une population de voisins
        population_voisins = [solution_actuelle]
        for _ in range(taille_population_rang - 1):
            population_voisins.append(generer_voisin(solution_actuelle))
        
        # Trier les voisins par qualité
        population_voisins_triee, distances_triees = evaluer_et_trier_population(population_voisins, matrice_distances)
        
        for _ in range(iterations_par_temperature):
            # Sélection par rang d'un voisin
            solution_voisine = selection_rang(population_voisins_triee, fitness_rang)
            distance_voisine = calcule_distance_totale(solution_voisine, matrice_distances)
            
            # Calculer la différence de coût
            delta = distance_voisine - distance_actuelle
            
            # Accepter la solution si elle est meilleure
            if delta < 0:
                solution_actuelle = solution_voisine
                distance_actuelle = distance_voisine
                
                if distance_voisine < meilleure_distance:
                    meilleure_solution = solution_voisine[:]
                    meilleure_distance = distance_voisine
                    
            # Accepter une solution pire avec une certaine probabilité
            else:
                probabilite = math.exp(-delta / temperature)
                if random.random() < probabilite:
                    solution_actuelle = solution_voisine
                    distance_actuelle = distance_voisine
        
        # Refroidissement
        temperature *= taux_refroidissement
    
    return meilleure_solution, meilleure_distance

# Matrice de distances
matrice_distances = [
    [0, 2, 3, 3, 7, 7, 0, 1, 7, 2],
    [2, 0, 10, 4, 7, 3, 7, 15, 8, 2],
    [3, 10, 0, 1, 4, 3, 3, 4, 2, 3],
    [3, 4, 1, 0, 2, 15, 7, 7, 5, 4],
    [7, 7, 4, 2, 0, 7, 3, 2, 2, 7],
    [7, 3, 3, 15, 7, 0, 1, 0, 2, 10],
    [0, 7, 3, 7, 3, 1, 0, 2, 1, 3],
    [1, 15, 4, 7, 2, 0, 2, 0, 1, 10],
    [7, 8, 2, 5, 2, 2, 1, 1, 0, 15],
    [2, 2, 3, 4, 7, 10, 3, 10, 15, 0]
]

print("=== ALGORITHME GÉNÉTIQUE AVEC SÉLECTION PAR RANG ===")
meilleure_solution_ga, meilleure_distance_ga = algorithme_genetique_rang(
    matrice_distances,
    taille_population=50,
    nombre_generations=1000,
    taux_mutation=0.2,
    pression_selection=1.5
)

print("\nMeilleure solution trouvée (Algorithme Génétique - Rang):", meilleure_solution_ga)
print("Distance minimale:", meilleure_distance_ga)

print("\n=== RECHERCHE SIMULÉE HYBRIDE AVEC RANG ===")
meilleure_solution_sa, meilleure_distance_sa = simulated_annealing_avec_rang(
    matrice_distances,
    temperature_initiale=1000,
    temperature_finale=0.1,
    taux_refroidissement=0.95,
    iterations_par_temperature=50,
    taille_population_rang=20
)

print("Meilleure solution trouvée (SA avec Rang):", meilleure_solution_sa)
print("Distance minimale:", meilleure_distance_sa)

# Affichage de la distribution des fitness par rang
print("\n=== DISTRIBUTION FITNESS PAR RANG (exemple pour population=10) ===")
fitness_exemple = calculer_fitness_par_rang(10, 1.5)
for i, fit in enumerate(fitness_exemple):
    print(f"Rang {i}: fitness = {fit:.3f}")
