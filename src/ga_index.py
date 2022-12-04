from ga_functions import *
from paramaters_ga import *


def limits(x1, x2):
    if 5*x1 + 2*x2 > 30:
        return False
    if 8*x1 + 11*x2 > 60:
        return False
    if x1 < 0:
        return False
    if x2 < 0:
        return False
    return True

f = lambda x1, x2: (2*x1 - 0.1*x1**2 + 3*x2 - 0.1*x2**2)
population = create_random_population(n_gen, n_hrom, initial_range, limits)# Начальная популяция

best_outputs = []
num_generations = 100 # Максимальное число итераций
s = 0
eps = 0.05
max = 0

for generation in range(num_generations):
    print(" ")
    print("Generation : ", generation) # номер поколения
    f_values = function_values(f, population) # значения функции в каждой хромосоме
    print("Population:  ", population) # популяция
    print("Function values: ", f_values) # значения функции
    parents = sorted(population, key=lambda tup: f(tup[0], tup[1]))[-1:-int(n_hrom*k):-1] # выбираем лучших, половину
    best_outputs = sorted(f_values)[-1:-int(n_hrom*k):-1]

    if max < best_outputs[0]:
        max = best_outputs[0]
        max_p = parents[0]

    print("Parents:  ", parents)
    print("Best output:  ", best_outputs)
    offspring = crossover(parents, n_hrom, n_gen, limits)
    print("Offspring:  ", offspring)
    print("Sorted Offspring: ", sorted(offspring, key=lambda tup: f(tup[0], tup[1]))[::-1])
    population = mutation(offspring, k_mutation, limits)
    print("Offspring after mutation:  ", offspring)
    print(" ")
    if best_outputs == []:
        break

print(max, max_p)