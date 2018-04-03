# The following python code is an implementation of a genetic algorithm
# that seeks to create a near-optimal schedule for a basketball camp.
# Details of the scenario can be seen in TeamCamp.pdf. A companion 
# SCHEDULE.TXT document should be placed in the same directory this 
# script is run from, which will give daily start and end times for each
# team, the team's rank (1-3), and whether it's varsity or JV or both.

import random
import numpy 
import array

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

# HyperParameters for GA:
num_of_gens = 40
pop_size = 100
tour_size = 3
mutpb = 0.2
cxpb = 0.5

# Schedule Parameters:
day1_start = 8 # Time in 24hr format by the hour
day1_end = 23 # Time start of last game is this -1
day2_start = 8
day2_end = 23

# Number of courts available in each location
loc1_courts = 5 # Main courts located @ mercer
loc2_courts = 2 # Ingleside courts
loc3_courts = 1 # Vineville Methodist Court
loc4_courts = 1 # Vineville Baptist Court

# Custom Crossover Function. Typical crossover functions will not work
# well for our structure, so a custom way to breed 2 schedules is
# desired. Plan for a custom cx: Parent 1 has 50/50 chan 
def schedule_cx(schedule1, schedule2):
    return schedule1, schedule2
    # Randomly pick a team, and locate it in first parent schedule.
    # Place all their scheduled times into new child schedule. Randomly
    # select another team, and copy it's schedule from the 2nd parent
    # into new child. Mend schedules if there is a conflict, but keep as
    # similar to the parent being adopted from as possible.

# Similar to CX, mutation needs to be a custom function to prevent
# completely breaking a schedule. Will try to do a smart mutation:
# Find team in schedule with lowest fitness. Modify one of its
# matches to attempt increasing fitness. Then run the repair 
# function to fix any conflicts.
def schedule_mut(schedule):
    return schedule,
    # Still working out the details...

# Our Fitness Function, determines how fit an individual is.
def calc_fitness(individual):
    return sum(individual), 
    # Psuedocode: Iterate through all the teams and figure out
    # the fitness of each. Sum up total fitness to calculate the
    # final schedule fitness. Staying at same facility, having
    # single hour gaps between games, and no scheduling conflicts
    # will yield a higer fitness.

# Generate a random schedule. This should be called in a loop.
def generate_schedule(team_list, conflict_list):
    random.seed()
    single_schedule = [1,2,3,4]
    return single_schedule
    # Psuedocode: pick a random team, and add them to a schedule.
    # Do this in a loop until all teams are added to a schedule.
    # Pick courts randomly, but start assigning the randomly picked
    # team at the earliest time they can be scheduled to play and
    # don't let them play back to back.

# Repair a schedule. This will be run after CX or MUT, to turn the
# schedule legal. No teams playing themselves or at 2 courts
# at the same time. No back to back games at different facilities.
# All teams within arrival and departure time. Also checks 
# conflicting_teams to make sure V and JV of same team isn't 
# scheduled during same time if this option was requested.
def repair_schedule(schedule):
    return schedule
    # Still working out the details...
# Main function to tie everything together.
def main():
    # We start by importing SCHEDULE.txt with each team specifics.
    print ("Importing team schedules")
    teams_to_schedule = []  # Master list of teams to schedule
    conflicting_teams = []  # Master list of teams that can't play at same time
    general_population = [] # Holds our current population of schedules
    with open("SCHEDULE.txt","r") as input_file:
        team_number = 1
        for line in input_file:
            if(len(line.strip()) == 0):
                continue
            single_data_line=line.strip().split("-")
            schedule_write = [] # Single line list to add to master list after setting

            # String has been split. Check if we're adding 1 or 2 teams to the schedule.
            # Teams with both a V and JV require two separate teams
            # Each team needs a unique number, issued by team_number

            if (single_data_line[1] == '1') or (single_data_line[1] == '2'):
                # Single Team Case
                if single_data_line[1] == '1':
                    single_data_line[0] = single_data_line[0] + " V"
                else:
                    single_data_line[0] = single_data_line[0] + " JV"
                # print (single_data_line[0], " has just a V or JV to play")
                schedule_write.append(single_data_line[0]) # Team Name
                schedule_write.append(team_number) # Unique Team Number
                schedule_write.append(int(single_data_line[1])) # 1 for V, 2 for JV
                schedule_write.append(int(single_data_line[3])) # Rank from 1-3
                schedule_write.append(int(single_data_line[4])) # Start time
                schedule_write.append(int(single_data_line[5])) # End time
                # print ("Importing :", schedule_write)
                teams_to_schedule.append(schedule_write)
            elif single_data_line[1] == '3':
                # Varsity and JV team, [2] will be Y if they can play at the same time
                if (single_data_line[2] == 'N') or (single_data_line[2] == 'n'):
                    # Add team numbers to conflict pool
                    add_conflict = []
                    add_conflict.append(team_number)
                    add_conflict.append(team_number+1)
                    conflicting_teams.append(add_conflict)
                # Parse rank structure for later addition to schedule_write
                parsed_rank=single_data_line[3].strip().split(",")
                # Create varsity team first
                temp_name_string = single_data_line[0] + " V"
                schedule_write.append(temp_name_string) # Team Name
                schedule_write.append(team_number) # Unique Team Number
                schedule_write.append(int(1)) # 1 for V, 2 for JV
                schedule_write.append(int(parsed_rank[0])) # Rank from 1-3
                schedule_write.append(int(single_data_line[4])) # Start time
                schedule_write.append(int(single_data_line[5])) # End time
                teams_to_schedule.append(schedule_write)
                # print ("Importing :", schedule_write)
                team_number +=1 # Increment our team counter for special case
                schedule_write = [] # Clear out our list to create 2nd JV team
                temp_name_string = single_data_line[0] + " JV"
                schedule_write.append(temp_name_string) # Team Name
                schedule_write.append(team_number) # Unique Team Number
                schedule_write.append(int(2)) # 1 for V, 2 for JV
                schedule_write.append(int(parsed_rank[1])) # Rank from 1-3
                schedule_write.append(int(single_data_line[4])) # Start time
                schedule_write.append(int(single_data_line[5])) # End time
                teams_to_schedule.append(schedule_write)
                # print ("Importing :", schedule_write)
                # print (single_data_line[0], " has both V and JV to play")
            else:
                print ("Problem with SCHEDULE.txt, please fix team named:",single_data_line[0])
                exit()
            # increment our team_number counter
            team_number += 1
    print("Import successful. Starting Genetic Algorithm.")
    # We are done reading our file in...
    # print("\n\nOur conflicting teams: ")
    # print(conflicting_teams)
    # print("Our individual teams: ")
    # print(teams_to_schedule)

    # Time to set up our Genetic Algo. We have a single objective for fitness,
    # which is to maximize it.
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))

    # So far an individual is a list, if we move to numpy we would change
    # list to numpy. Link our fitness to individual. Typecode I = unsigned int
    creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMax)

    # Initialize our toolbox
    toolbox = base.Toolbox()

    # Register our individual and population, call custom individual creation function
    toolbox.register("individual", creator.Individual, 
            generate_schedule(teams_to_schedule, conflicting_teams))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # Register custom evaluate, mutate, and crossover. Use tournament selection.
    toolbox.register("evaluate", calc_fitness)
    toolbox.register("mate", schedule_cx)
    toolbox.register("mutate", schedule_mut)
    toolbox.register("select", tools.selTournament, tournsize=tour_size)
    
    # After everything has been set, register stats and run gen algo
    random.seed(128)
    pop = toolbox.population(n=pop_size)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    # print("\n\n")
    # print (pop[1])
    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=cxpb, mutpb=mutpb, ngen=num_of_gens,
            stats=stats, halloffame=hof, verbose=True)

    return pop, log, hof
if __name__ == "__main__":
    main()
