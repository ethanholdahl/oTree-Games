from otree.api import *
import random
import numpy as np
import re
doc = """
This is a repeated "Prisoner's Dilemma" against the same opponent each round.
Two players are asked separately whether they want to cooperate or defect.
Their choices directly determine the payoffs.
"""


class C(BaseConstants):
    NAME_IN_URL = 'stepping_stones'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    INSTRUCTIONS_TEMPLATE = 'stepping_stones/instructions.html'
    PAYOFF_A = cu(7)
    PAYOFF_B = cu(1)
    PAYOFF_C = cu(7)
    PAYOFF_D = cu(1)
    PAYOFF_E = cu(1)
    PAYOFF_F = cu(1)
    PAYOFF_G = cu(1)
    PAYOFF_H = cu(1)
    PAYOFF_I = cu(9)
    UPDATE = .5
    ROUNDS = 15
    PLOT_TEMPLATE = __name__ + '/Plot.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    randomized = models.IntegerField(
    initial = 0
    )

class Player(BasePlayer):
    choice = models.CharField(
        choices = [['A', 'A'], ['B', 'B'], ['C', 'C']],
        doc = "This player's decision",
        widget = widgets.RadioSelect,
        initial = 'A'
    )
    choice_history = models.LongStringField(
    initial = 'A'
    )
    strategy = models.CharField(
    initial = 'A'
    )
    strategy_history = models.LongStringField(
    initial = 'A'
    )
    payoff_history = models.LongStringField(
    initial = '0'
    )
    round = models.IntegerField(
    initial = '0'
    )
    change = models.CharField(
    initial = 'true'
    )

# FUNCTIONS

def count_strategies(group: Group):
    players = group.get_players()
    strategies = [p.strategy for p in players]
    totals = [strategies.count("A"), strategies.count("B"), strategies.count("C")]
    return totals



def set_payoffs(group: Group):
    for player in group.get_players():
        payoff_matrix = ([
        C.PAYOFF_A,
        C.PAYOFF_D,
        C.PAYOFF_G],
        [C.PAYOFF_B,
        C.PAYOFF_E,
        C.PAYOFF_H],
        [C.PAYOFF_C,
        C.PAYOFF_F,
        C.PAYOFF_I])
        if player.strategy == "A":
            play = count_strategies(group)
            play[0] = play[0]-1
            payoff = np.dot(play,payoff_matrix)[0]
        if player.strategy == "B":
            play = count_strategies(group)
            play[1] = play[1]-1
            payoff = np.dot(play,payoff_matrix)[1]
        if player.strategy == "C":
            play = count_strategies(group)
            play[2] = play[2]-1
            payoff = np.dot(play,payoff_matrix)[2]
        player.payoff = payoff


def custom_export(players):
    # header row
    yield ['session', 'participant_code', 'id_in_group', 'payoff', 'choice_history', 'strategy_history', 'payoff_history']
    for p in players:
        yield [p.session.code, p.participant.code, p.id_in_group, p.payoff, p.choice_history, p.strategy_history, p.payoff_history]


# PAGES
class Introduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class ExperimentWaitPage(WaitPage):
    pass




class Experiment(Page):
    #timeout_seconds = 2065

    #@staticmethod
    #def js_vars(player: Player):
    #    return dict(my_id=player.id_in_group, choice=player.choice)

    @staticmethod
    def live_method(player: Player, data):
        group = player.group
        if 'choice' in data:
            player.choice = data['choice']
            return {player.id_in_group: dict(
            choice = player.choice
            )}
        if data == 'calculate':
            #End of round
            #Do stochastic determination for all players during first pass.
            if group.randomized == 0:
                for p in group.get_players():
                    #record choice
                    p.choice_history = p.choice_history + "," +p.choice
                    #determine if choice is stochastically accpeted
                    if random.random() > C.UPDATE:
                        #action changed fails
                        p.change = "false"
                        p.strategy = p.strategy_history[-1]
                    else:
                        p.change = "true"
                        p.strategy = p.choice
                    #update player.strategy_history
                    p.strategy_history = p.strategy_history + "," + p.strategy
                #calculate round payoff
                set_payoffs(group)
            # reset group.randomized once the last player runs this code
            group.randomized += 1
            if (group.randomized == len(group.get_players())):
                group.randomized = 0
            #store payoff, advance round number, and collect other players strategies
            player.payoff_history = player.payoff_history + "," + str(player.payoff)
            player.round = player.round + 1
            if player.strategy == "A":
                play = count_strategies(group)
                play[0] = play[0]-1
            if player.strategy == "B":
                play = count_strategies(group)
                play[1] = play[1]-1
            if player.strategy == "C":
                play = count_strategies(group)
                play[2] = play[2]-1
            #check if finished and return data to page
            if player.round >= C.ROUNDS:
                finished = "true"
            else:
                finished = "false"
            if (player.change == "true"):
                message = "".join(["Your choice last round, ", player.choice, ", was randomly accpeted and your strategy was updated. Consequently, your strategy for last round is ", player.choice, "."])
            else:
                message = "".join(["Your choice last round, ", player.choice, ", was randomly rejected and your strategy failed to update. Consequently, your strategy for last round is ", player.strategy, "."])
            #set player.choice to player.strategy
            player.choice = player.strategy
            if (player.strategy == "A"):
                payoff_message = "".join([str(play[0])," * ",str(C.PAYOFF_A)," + ",str(play[1])," * ",str(C.PAYOFF_B)," + ",str(play[2])," * ",str(C.PAYOFF_C)," = ",str(player.payoff)])
            if (player.strategy == "B"):
                payoff_message = "".join([str(play[0])," * ",str(C.PAYOFF_D)," + ",str(play[1])," * ",str(C.PAYOFF_E)," + ",str(play[2])," * ",str(C.PAYOFF_F)," = ",str(player.payoff)])
            if (player.strategy == "C"):
                payoff_message = "".join([str(play[0])," * ",str(C.PAYOFF_G)," + ",str(play[1])," * ",str(C.PAYOFF_H)," + ",str(play[2])," * ",str(C.PAYOFF_I)," = ",str(player.payoff)])

            return {player.id_in_group: dict(
            message=message,
            strategy=player.strategy,
            payoff_message=payoff_message,
            play=play,
            finished=finished
            )}



class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        payoffrounds = random.sample(range(1,(C.ROUNDS+1)), k = 3)
        payoffround1 = payoffrounds[0]
        payoffround2 = payoffrounds[1]
        payoffround3 = payoffrounds[2]
        values = player.payoff_history.split(',')
        payoff1 = values[payoffround1]
        payoff2 = values[payoffround2]
        payoff3 = values[payoffround3]
        player.payoff = float(re.sub("[^0-9]", "", payoff1)) + float(re.sub("[^0-9]", "",payoff2)) + float(re.sub("[^0-9]", "",payoff3))
        #player.payoff = payoff1 + payoff2 + payoff3
        return dict(
        payoffround1 = payoffround1,
        payoffround2 = payoffround2,
        payoffround3 = payoffround3,
        payoff1 = payoff1,
        payoff2 = payoff2,
        payoff3 = payoff3
        )



#page_sequence = [Introduction, Decision, ResultsWaitPage, Results]
page_sequence = [Introduction, ExperimentWaitPage, Experiment, Results]
