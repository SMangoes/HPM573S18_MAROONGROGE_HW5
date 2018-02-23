#HW 5 problems 1 and 2
#Sean Maroongroge

from enum import Enum
import numpy as np
import scr.FigureSupport as FigSupport


#define variables
COST_TO_PLAY = 250
GAIN_PER_WIN = 100

#enumerate heads and tails
class Flip_Result(Enum):
    HEADS = 1
    TAILS = 0

#flip a single coin
class single_flip:
    def __init__(self, flip_id, prob_of_heads):
        self._flip_id = flip_id
        self._rnd = np.random
        self._rnd.seed(flip_id)
        self._flip_result = Flip_Result.HEADS
        self.prob_of_heads = prob_of_heads

    def simulate(self):
        if self._rnd.sample() < self.prob_of_heads:
            self._flip_result = Flip_Result.TAILS
        else:
            self._flip_result = Flip_Result.HEADS

    def get_single_flip_result(self):
        return self._flip_result  #note: if I use this function and try to print the object, I get the memory pointer and not the actual result variable, so just ignore this function for now


#create a cohort (list) of coins within 1 game
class cohort_of_flips:
    def __init__(self, cohort_id, number_of_flips, prob_of_heads):
        self._cohort_id = cohort_id
        self._number_of_flips = number_of_flips
        self._list_of_flips = [] #just populate a list with flip objects (with unique IDs)
        self._list_of_flip_results = [] #populate another list with flip results
        self._cohort_reward_amount = 0


        #populate the list with the single flip objects (no results)
        for flip_number in range(number_of_flips):
            flip = single_flip(cohort_id*number_of_flips + flip_number, prob_of_heads=prob_of_heads)
            self._list_of_flips.append(flip)

    def simulate(self):

        #populate the list of flip results
        for flip in self._list_of_flips:
            flip.simulate()                  #remember you actually need to run the simulation..
            self._list_of_flip_results.append(flip._flip_result) #append the result
            #print (flip._flip_result)

        #calculate the total reward amount for this list
        self._cohort_reward_amount = -COST_TO_PLAY #start at -250

        #for each "win", add 100 to reward
        self._list_of_flip_results_length = len(self._list_of_flip_results)
        for index, obj in enumerate(self._list_of_flip_results):
            if index > 1:
                self._super_previous_item = self._list_of_flip_results[index - 2]
                self._previous_item = self._list_of_flip_results[index - 1]
                if obj.value == 1 and self._super_previous_item.value ==0 and self._previous_item.value ==0:
                #    print("trial number", index, obj.value, self._super_previous_item.value, self._previous_item.value, "this is a win")
                    self._cohort_reward_amount += 100

                #remember with enumerate to call object values as opposed to objects themselves, using obj.value==1, not obj==1
                #if obj.value ==1:
                #    print('obj is equal to 1')
                #if obj.value ==0:
                #    print('obj is equal to 0')

    #return the reward amount for this single game (single cohort of flips)
    def get_cohort_reward_amount(self):
        return self._cohort_reward_amount


#simulate 1000 games

class cohort_of_games:
    #create the list of games that happened
    def __init__(self, number_of_games, number_of_flips, prob_of_heads):
        self._number_of_flips = number_of_flips #maybe not needed
        self._number_of_games = number_of_games
        self._list_of_games = []
        self._list_of_game_rewards = []
        self._overall_lost_money_counter = 0

        for game_id in range(self._number_of_games):
            ThisCohortofFlips = cohort_of_flips(cohort_id = game_id, number_of_flips = self._number_of_flips, prob_of_heads=prob_of_heads)
            ThisCohortofFlips.simulate()
            self._list_of_games.append(ThisCohortofFlips)

    #simulate the games to generate the list of rewards for all 1000 games in a list
    def simulate(self):
        for game in self._list_of_games:
            self._list_of_game_rewards.append(game.get_cohort_reward_amount())

    #calculate and return the average of this list of rewards over the entire simulation
    def get_average_reward_amount(self):
        average_reward_amount = sum(self._list_of_game_rewards)/len(self._list_of_game_rewards)
        return average_reward_amount

    #get list of game rewards (NOT the average), because histogram requires just the list
    def get_list_of_game_rewards(self):
        return self._list_of_game_rewards

    def get_loss_probability(self):
        for game_result in self._list_of_game_rewards:
            if game_result < 0:
                self._overall_lost_money_counter += 1
        return self._overall_lost_money_counter/1000 * 100

myCohortofGames = cohort_of_games(number_of_games=1000, number_of_flips=20, prob_of_heads=0.4)
myCohortofGames.simulate()
print(myCohortofGames.get_average_reward_amount())


#PROBLEM 1
#create histogram of reward amounts, note the input requires the list of rewards
FigSupport.graph_histogram(
    observations=myCohortofGames.get_list_of_game_rewards(),
    title="Histogram of reward amounts",
    x_label="reward amount",
    y_label="number of trials"
)

#PROBLEM 2
#In 1000 trials, what's the probability of losing money?
#formula is prob = # of trials with reward <0 / 1000

print(myCohortofGames.get_loss_probability(),"% chance of losing money")
