import random
import math
def calcule_distance_totale(solution, matrice_distances):
    """Calcule la distance totale d'un cycle de villes"""
    distance_totale = 0
    n = len(solution)
    
    for i in range(n - 1):
        distance_totale += matrice_distances[solution[i]][solution[i + 1]]
    
    # Retour à la ville de départ
    distance_totale += matrice_distances[solution[-1]][solution[0]]
    
    return distance_totale


def generer_voisin(solution):
    """Génère un voisin aléatoire en échangeant deux villes"""
    voisin = solution[:]  # Copie de la solution
    i, j = random.sample(range(len(solution)), 2)
    voisin[i], voisin[j] = voisin[j], voisin[i]
    return voisin


def simulated_annealing(matrice_distances, temperature_initiale, temperature_finale, 
                       taux_refroidissement, iterations_par_temperature):
    """Implémente l'algorithme du recuit simulé pour le problème du voyageur de commerce"""
    
    nombre_villes = len(matrice_distances)
    
    solution_actuelle = list(range(nombre_villes))
    random.shuffle(solution_actuelle)
    distance_actuelle = calcule_distance_totale(solution_actuelle, matrice_distances)
    
    meilleure_solution = solution_actuelle[:]
    meilleure_distance = distance_actuelle
    
    temperature = temperature_initiale
    
    while temperature > temperature_finale:
        for _ in range(iterations_par_temperature):
            # Générer un voisin aléatoire
            solution_voisine = generer_voisin(solution_actuelle)
            distance_voisine = calcule_distance_totale(solution_voisine, matrice_distances)
            
            delta = distance_voisine - distance_actuelle
            
            if delta < 0:
                solution_actuelle = solution_voisine
                distance_actuelle = distance_voisine
                
                # Mettre à jour la meilleure solution
                if distance_voisine < meilleure_distance:
                    meilleure_solution = solution_voisine[:]
                    meilleure_distance = distance_voisine
            
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

temperature_initiale = 1000
temperature_finale = 0.1
taux_refroidissement = 0.95
iterations_par_temperature = 100

# Exécution de l'algorithme
meilleure_solution, meilleure_distance = simulated_annealing(
    matrice_distances, 
    temperature_initiale, 
    temperature_finale, 
    taux_refroidissement, 
    iterations_par_temperature
)

print("Meilleure solution trouvée (Recuit Simulé):", meilleure_solution)
print("Distance minimale:", meilleure_distance)
