import random
import math

def calcule_distance_totale(solution, matrice_distances):
    distance_totale = 0
    for i in range(len(solution) - 1):
        distance_totale += matrice_distances[solution[i]][solution[i + 1]]
    distance_totale += matrice_distances[solution[-1]][solution[0]]
    return distance_totale

def generer_voisin(solution):
    """ je veux générer ici   un voisin aléatoire en échangeant deux villes"""
    voisin = solution[:]
    i, j = random.sample(range(len(solution)), 2)
    voisin[i], voisin[j] = voisin[j], voisin[i]
    return voisin

def generer_population_initial(taille_population, nombre_villes):
    """ je veux générer ici  une population initiale de solutions aléatoires"""
    population = []
    for _ in range(taille_population):
        solution = list(range(nombre_villes))
        random.shuffle(solution)
        population.append(solution)
    return population

def evaluer_population(population, matrice_distances):
    """ je veux faire ici l’évaluation de  la fitness de chaque solution """
    distances = []
    fitness = []
    
    for solution in population:
        distance = calcule_distance_totale(solution, matrice_distances)
        distances.append(distance)
        # Pour la minimisation  on utilise l'inverse de la distance comme fitness
        fitness.append(1 / (distance + 1))  # +1 pour éviter division par zéro
    
    return distances, fitness

def selection_roulette(population, fitness):
    """Sélectionne une solution selon la méthode de la roulette"""
    fitness_totale = sum(fitness)
    if fitness_totale == 0:
        return random.choice(population)
    
    # je veux ici  Générer un nombre aléatoire entre 0 et fitness_totale
    valeur_aleatoire = random.uniform(0, fitness_totale)
    
    # je veux ici Parcourir la population pour trouver la solution sélectionnée
    somme_cumulee = 0
    for i in range(len(population)):
        somme_cumulee += fitness[i]
        if somme_cumulee >= valeur_aleatoire:
            return population[i][:]  # Retourne une copie
    
    # En cas d'erreur, il va retourner la dernière solution
    return population[-1][:]

def algorithme_genetique_roulette(matrice_distances, taille_population, nombre_generations, taux_mutation):
    nombre_villes = len(matrice_distances)
    
    
    population = generer_population_initial(taille_population, nombre_villes)
    
    meilleure_solution = None
    meilleure_distance = float('inf')
    
    for generation in range(nombre_generations):
        # je veux faire ici l’évaluation de la population
        distances, fitness = evaluer_population(population, matrice_distances)
        
        # je veux faire ici la Mise à jour de la meilleure solution
        for i in range(len(population)):
            if distances[i] < meilleure_distance:
                meilleure_solution = population[i][:]
                meilleure_distance = distances[i]
        
        # je veux faire ici la Création d'une nouvelle population par sélection par roulette
        nouvelle_population = []
        
        # je veux ici conserver la meilleure solution
        nouvelle_population.append(meilleure_solution[:])
        
        while len(nouvelle_population) < taille_population:
            # Sélection par roulette
            parent = selection_roulette(population, fitness)
            
            # Mutation
            if random.random() < taux_mutation:
                enfant = generer_voisin(parent)
            else:
                enfant = parent[:]
            
            nouvelle_population.append(enfant)
        
        population = nouvelle_population
        
        # Affichage de progression
        if generation % 100 == 0:
            print(f"Génération {generation}: Meilleure distance = {meilleure_distance}")
    
    return meilleure_solution, meilleure_distance

def simulated_annealing_avec_roulette(matrice_distances, temperature_initiale, temperature_finale, 
                                    taux_refroidissement, iterations_par_temperature, taille_population_roulette):
    """Version hybride avec sélection par roulette pour générer les voisins"""
    
    nombre_villes = len(matrice_distances)
    
    # Solution initiale aléatoire
    solution_actuelle = list(range(nombre_villes))
    random.shuffle(solution_actuelle)
    distance_actuelle = calcule_distance_totale(solution_actuelle, matrice_distances)
    
    meilleure_solution = solution_actuelle[:]
    meilleure_distance = distance_actuelle
    
    temperature = temperature_initiale
    
    while temperature > temperature_finale:
        # Générer une population de voisins pour la sélection par roulette
        population_voisins = [solution_actuelle]
        for _ in range(taille_population_roulette - 1):
            population_voisins.append(generer_voisin(solution_actuelle))
        
        # Évaluer les voisins
        distances_voisins, fitness_voisins = evaluer_population(population_voisins, matrice_distances)
        
        for _ in range(iterations_par_temperature):
            # Sélection par roulette d'un voisin
            solution_voisine = selection_roulette(population_voisins, fitness_voisins)
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

print("=== ALGORITHME GÉNÉTIQUE AVEC SÉLECTION PAR ROULETTE ===")
meilleure_solution_ga, meilleure_distance_ga = algorithme_genetique_roulette(
    matrice_distances,
    taille_population=50,
    nombre_generations=1000,
    taux_mutation=0.3
)

print("\nMeilleure solution trouvée (Algorithme Génétique):", meilleure_solution_ga)
print("Distance minimale:", meilleure_distance_ga)

print("\n=== RECHERCHE SIMULÉE HYBRIDE AVEC ROULETTE ===")
meilleure_solution_sa, meilleure_distance_sa = simulated_annealing_avec_roulette(
    matrice_distances,
    temperature_initiale=1000,
    temperature_finale=0.1,
    taux_refroidissement=0.95,
    iterations_par_temperature=50,
    taille_population_roulette=20
)

print("Meilleure solution trouvée (SA avec Roulette):", meilleure_solution_sa)
print("Distance minimale:", meilleure_distance_sa)
