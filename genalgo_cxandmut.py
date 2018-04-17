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

# USER EDITABLE VARIABLES
# HyperParameters for GA:
num_of_gens = 50 # 1 # 40
pop_size = 50 #100
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

# DO NOT EDIT BELOW
# Required global variables for our functions to work
num_of_teams = 0 # Default to 0, populate later
num_of_conflicts = 0 # Incremented as we gain more conflicts
tot_courts = loc1_courts + loc2_courts + loc3_courts + loc4_courts
day1_slots = day1_end - day1_start
day2_slots = day2_end - day2_start
tot_slots = day1_slots + day2_slots


# Custom Crossover Function. Typical crossover functions will not work
# well for our structure, so a custom way to breed 2 schedules is
# desired. Plan for a custom cx: Parent 1 has 50/50 chan 
def schedule_cx(schedule1, schedule2):
    temp_hold = schedule1[0][0][0]
    schedule1[0][0][0] = schedule2[0][0][0]
    schedule2[0][0][0] = temp_hold
    # temp_hold = schedule1[0][0][1]
    # schedule1[0][0][1] = schedule2[0][0][1]
    # schedule2[0][0][1] = temp_hold
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
    schedule[0][0][0] += 1
    schedule[0][0][1] -= 1
    return schedule,
    # Still working out the details...

# Our Fitness Function, determines how fit an individual is.
def calc_fitness(individual):
    total_fit = individual[0][0][0] + individual[0][0][1]
    return total_fit,
    # return 11,
    # return sum(individual), 
    # Psuedocode: Iterate through all the teams and figure out
    # the fitness of each. Sum up total fitness to calculate the
    # final schedule fitness. Staying at same facility, having
    # single hour gaps between games, and no scheduling conflicts
    # will yield a higer fitness.

# Used during initial blank schedule creation, creates one time
# slot worth of courts to schedule games on
def single_slot():
    one_match = [0,0]
    one_timeslot = []
    for i in range(tot_courts):
        one_timeslot.append(one_match[:])
    return one_timeslot[:]

# Generate a random schedule. This should be called in a loop.
def generate_schedule(population, team_list, conflict_list):
    # Create a reference to our population to easily edit it
    scheduled_pop = population
    # References to our population are as follows:
    # pop[Individual][TimeSegment][Court][TeamSide]
    for h in range(pop_size):
        # Generate order of teams to populate schedule randomly
        team_order_list = random.sample(range(1,num_of_teams+1,1), k=num_of_teams)
        print("Team Order List Is: ", team_order_list)
        print("h is: ", h)
        scheduled_pop[h][0][0][0] = team_order_list[0]
        scheduled_pop[h][0][0][1] = team_order_list[1]
        # Start iterating through team_order_list and populating schedule
        #for team in team_order_list:
            # print("Team is: ", team)
            # Check if team is in our conflict list. If so, schedule its 
            # conflict at the same time for simplicity
            # print("Scheduling team: ", team)
            # scheduled_pop[h][0][0] = team
    # single_schedule = [1,2,3,4]
    # single_schedule[0][0] = team_order_list[0]
    return scheduled_pop
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
    # Seed our random number generator
    random.seed(random.SystemRandom().random())
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
                    global num_of_conflicts
                    num_of_conflicts += 1
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
            # store off current team number (also # of teams imported)
            global num_of_teams
            num_of_teams = team_number
            # increment our team_number counter
            team_number += 1
    print("Number of teams to schedule: ", num_of_teams)
    print("Import successful. Starting Genetic Algorithm.")
    # We are done reading our file in...
    # print("\n\nOur conflicting teams: ")
    # print(conflicting_teams)
    print("Our individual teams: ")
    print(teams_to_schedule)

    # Time to set up our Genetic Algo. We have a single objective for fitness,
    # which is to maximize it.
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))

    # Our individual is a list (with nested lists, needs not be specified)
    creator.create("Individual", list, fitness=creator.FitnessMax)

    # Initialize our toolbox
    toolbox = base.Toolbox()

    # Register our individual and population, call custom individual creation function.
    # Single_help is used to prevent the same ID being used, and creates individual
    # hourly time slots for all courts
    toolbox.register("single_help", single_slot)
    toolbox.register("individual", tools.initRepeat, creator.Individual, 
           toolbox.single_help, tot_slots)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # Register custom evaluate, mutate, and crossover. Use tournament selection.
    toolbox.register("evaluate", calc_fitness)
    toolbox.register("mate", schedule_cx)
    toolbox.register("mutate", schedule_mut)
    toolbox.register("select", tools.selTournament, tournsize=tour_size)
    
    pop = toolbox.population(n=pop_size)
    # References to our population are as follows:
    # pop[Individual][TimeSegment][Court][TeamSide]
    # eg pop[4][0][0][0] would reference the 5th individual schedule, first time
    # slot, first court, and the first team scheduled for that court.
    generate_schedule(pop, teams_to_schedule, conflicting_teams)
    print("Initial population successfully generated")
    # print("Member 1: \n", list(map(id,pop[0])))
    # print("Member 2: \n", list(map(id,pop[1])))
    # print("Member 3: \n", list(map(id,pop[2])))
    hof = tools.HallOfFame(1)

    # After everything has been set, register stats and run gen algo
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=cxpb, mutpb=mutpb, ngen=num_of_gens,
            stats=stats, halloffame=hof, verbose=True)

    return pop, log, hof
if __name__ == "__main__":
    main()
