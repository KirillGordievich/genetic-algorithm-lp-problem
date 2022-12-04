import random


def create_random_population(n_gen, n_hrom, initial_range, constraints):
    population = []

    for j in range(n_hrom):
        hromosom = [round(random.uniform(initial_range[0], initial_range[1]), 2)
                    for i in range(n_gen)]
        while constraints(*hromosom) is False:
            hromosom = [round(random.uniform(initial_range[0], initial_range[1]), 2)
                        for i in range(n_gen)]
        population.append(hromosom)
    return population

def function_values(f, population):
    return [f(*i) for i in population]

def crossover(parents, n_hrom, n_gen, constraints):
    offspring = []

    if n_gen == 2:
        s = 0
        while s < 2*n_hrom:
            i, j = random.sample(range(0, len(parents)), 2)
            p1, p2, = parents[i], parents[j]
            a = random.uniform(-1, 1)
            c1 = [a * p1[0] + (1 - a) * p2[0], a * p1[1] + (1 - a) * p2[1]]
            c2 = [-a * p2[0] + (1 + a) * p1[0], -a * p2[1] + (1 + a) * p1[1]]

            if constraints(*c1) is not False and c1 not in offspring:
                offspring.append(c1)
                if constraints(*c2) is not False and c2 not in offspring:
                    offspring.append(c2)
            if len(offspring) >= len(parents):
                break
            s += 1
    if n_gen == 3:
        j = 0
        max_steps = 5

        while len(offspring) < len(parents) and j < 5*n_hrom:
            s = 0
            i, j = random.sample(range(0, len(parents)), 2)
            p1, p2 = parents[i], parents[j]
            flag_c1 = False
            flag_c2 = False

            while s < max_steps:
                a = random.uniform(-1, 1)

                if flag_c1 == False:
                    c1 = [a*p1[0]+(1-a)*p2[0], a*p1[1]+(1-a)*p2[1], a*p1[2]+(1-a)*p2[2]]
                if flag_c2 == False:
                    c2 = [-a*p2[0]+(1+a)*p1[0], -a*p2[1]+(1+a)*p1[1], -a*p2[2]+(1+a)*p1[2]]
                if constraints(*c1) is not False or constraints(*c2) is not False:
                    if constraints(*c1) is not False and c1 not in offspring:
                        flag_c1 = True
                    if constraints(*c2) is not False and c2 not in offspring:
                        flag_c2 = True
                if flag_c1 and flag_c2 is True:
                    break
                s += 1
            if flag_c1:
                offspring.append(c1)
            if flag_c2:
                offspring.append(c2)
            j += 1
    return offspring

def mutation(population, h, constraints):
    eps = 0.05

    for i in range(len(population)):
        if random.randint(0, 1) == 1:
            new_population = list([i[:] for i in population])

            for j in range(len(population[i])):
                direction = random.choice([-1, 1])
                new_population[i][j] += direction * random.uniform(0, h)
                flag = True

                while constraints(*new_population[i]) is False:
                    new_population[i][j] = population[i][j]
                    h = h * 0.5
                    new_population[i][j] += direction * h
                    if h < eps and constraints(*new_population[i]) is False:
                        flag = False
                if flag:
                    population[i][j] = new_population[i][j]
    return population