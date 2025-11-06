import random
import math

class Particule:
    def __init__(self, dimensions, borne_min, borne_max):
        self.dimensions = dimensions
        self.position = [random.uniform(borne_min, borne_max) for _ in range(dimensions)]
        self.velocity = [random.uniform(-1, 1) for _ in range(dimensions)]
        self.best_position = self.position[:]
        self.best_fitness = float('inf')
        self.fitness = float('inf')
    
    def mettre_a_jour(self, meilleure_globale_position, w, c1, c2, borne_min, borne_max):
        for i in range(self.dimensions):
            r1 = random.random()
            r2 = random.random()
            
            composante_inertie = w * self.velocity[i]
            composante_personnelle = c1 * r1 * (self.best_position[i] - self.position[i])
            composante_sociale = c2 * r2 * (meilleure_globale_position[i] - self.position[i])
            
            self.velocity[i] = composante_inertie + composante_personnelle + composante_sociale
            self.position[i] += self.velocity[i]
            
            if self.position[i] < borne_min:
                self.position[i] = borne_min
                self.velocity[i] *= -0.5
            elif self.position[i] > borne_max:
                self.position[i] = borne_max
                self.velocity[i] *= -0.5

def PSO(fonction_objectif, dimensions=2, taille_essaim=20, iterations=50, 
        w=0.7, c1=1.5, c2=1.5, borne_min=-5, borne_max=5):
    
    essaim = [Particule(dimensions, borne_min, borne_max) for _ in range(taille_essaim)]
    
    meilleure_globale_position = essaim[0].position[:]
    meilleure_globale_fitness = float('inf')
    
    historique_fitness = []
    
    print("Début PSO")
    
    for iteration in range(iterations):
        w_actuel = w * (1 - iteration/iterations)
        
        for particule in essaim:
            particule.fitness = fonction_objectif(particule.position)
            
            if particule.fitness < particule.best_fitness:
                particule.best_position = particule.position[:]
                particule.best_fitness = particule.fitness
            
            if particule.fitness < meilleure_globale_fitness:
                meilleure_globale_position = particule.position[:]
                meilleure_globale_fitness = particule.fitness
        
        for particule in essaim:
            particule.mettre_a_jour(meilleure_globale_position, w_actuel, c1, c2, borne_min, borne_max)
        
        historique_fitness.append(meilleure_globale_fitness)
        
        if iteration % 10 == 0:
            print(f"Itération {iteration}: Fitness = {meilleure_globale_fitness:.4f}")
    
    print(f"Résultat: Fitness = {meilleure_globale_fitness:.6f}")
    print(f"Position: {[f'{x:.3f}' for x in meilleure_globale_position]}")
    
    return meilleure_globale_position, meilleure_globale_fitness, historique_fitness

def fonction_carre(x):
    return x[0]**2 + x[1]**2

print("=== OPTIMISATION FONCTION CARRÉ ===")
print("f(x,y) = x² + y²")
print("Minimum en (0,0) avec f(0,0)=0")

meilleure_position, meilleure_fitness, historique = PSO(
    fonction_carre,
    dimensions=2,
    taille_essaim=15,
    iterations=30,
    borne_min=-3,
    borne_max=3
)

print(f"\nSolution trouvée: ({meilleure_position[0]:.4f}, {meilleure_position[1]:.4f})")
print(f"Valeur optimale: {meilleure_fitness:.8f}")