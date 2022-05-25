from otree.api import *
import random
import numpy as np
import re
from datetime import datetime, timezone
doc = """
This is a repeated coordination game used to test the effectiveness of stepping stones.
"""

class C(BaseConstants):
    NAME_IN_URL = 'stepping_stones'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    INSTRUCTIONS_TEMPLATE = 'stepping_stones/instructions.html'
    PLOT_TEMPLATE = __name__ + '/Plot.html'


class Subsession(BaseSubsession):
    GAME = models.IntegerField(
    initial = 1
    )
    INFORMATION = models.BooleanField(
    initial = True
    )
    UPDATE = models.FloatField(
    initial = .5
    )
    ROUNDS = models.IntegerField(
    initial = 15
    )
    PLAYERS = models.IntegerField(
    initial = 8
    )
    OPPONENTS = models.IntegerField(
    initial = 7
    )
    PAYOFF_A = models.CurrencyField(
    initial = 7
    )
    PAYOFF_B = models.CurrencyField(
    initial = 1
    )
    PAYOFF_C = models.CurrencyField(
    initial = 7
    )
    PAYOFF_D = models.CurrencyField(
    initial = 1
    )
    PAYOFF_E = models.CurrencyField(
    initial = 1
    )
    PAYOFF_F = models.CurrencyField(
    initial = 1
    )
    PAYOFF_G = models.CurrencyField(
    initial = 1
    )
    PAYOFF_H = models.CurrencyField(
    initial = 1
    )
    PAYOFF_I = models.CurrencyField(
    initial = 9
    )
    EXA = models.CurrencyField(
    initial = 21
    )
    EXB = models.CurrencyField(
    initial = 3
    )
    EXC = models.CurrencyField(
    initial = 19
    )
    question1 = models.LongStringField(
    initial = "If your <font color='GREEN'><b>strategy</b></font> in a round is <font color='GREEN'><b>A</b></font> and the <font color='#0000FF'><b>strategy</b></font> of another player is <font color='#0000FF'><b>C</b></font> what <font color='FireBrick'><b>payoff</b></font> do you get for playing against them that round?"
    )
    solution1 = models.IntegerField(
    initial = '7'
    )
    question12 = models.LongStringField(
    initial = "If your <font color='GREEN'><b>strategy</b></font> in a round is <font color='GREEN'><b>C</b></font> and the <font color='#0000FF'><b>strategy</b></font> of another player is <font color='#0000FF'><b>B</b></font> what <font color='DarkBlue'><b>payoff</b></font> do they get for playing against you that round?"
    )
    solution12 = models.IntegerField(
    initial = '1'
    )
    question2 = models.LongStringField(
    initial = "Assume your <font color='GREEN'><b>strategy</b></font> last round was <font color='GREEN'><b>B</b></font>, your <font color='GoldenRod'><b>choice</b></font> this round is <font color='GoldenRod'><b>A</b></font>, and the <font color='#0000FF'><b>strategy</b></font> of another player this round is <font color='#0000FF'><b>A</b></font>. What is the smallest <font color='FireBrick'><b>payoff</b></font> you could get for playing againt them this round?"
    )
    solution2 = models.IntegerField(
    initial = '1'
    )
    question3 = models.LongStringField(
    initial = "Assume your <font color='GREEN'><b>strategy</b></font> last round was <font color='GREEN'><b>B</b></font>, your <font color='GoldenRod'><b>choice</b></font> this round is <font color='GoldenRod'><b>A</b></font>, the <font color='#0000FF'><b>strategy</b></font> of another player last round is <font color='#0000FF'><b>B</b></font>, and their <b>choice</b> this round is <b>C</b>. What is the largest <font color='FireBrick'><b>payoff</b></font> you could get for playing againt them this round?"
    )
    solution3 = models.IntegerField(
    initial = '7'
    )
    question4 = models.LongStringField(
    initial = "Assume there are 7 players other than you in the game, your <font color='GREEN'><b>strategy</b></font> in a round is <font color='GREEN'><b>A</b></font> and the distribution of opponents <font color='#0000FF'><b>strategies</b></font> are as follows: <font color='#0000FF'><b>2 A</b></font>, <font color='#0000FF'><b>4 B</b></font>, <font color='#0000FF'><b>1 C</b></font>. What would your <font color='Red'><b>payoff</b></font> for this round be?"
    )
    solution4 = models.IntegerField(
    initial = '25'
    )
    now_ms = models.IntegerField(
    initial = '1'
    )
    send = models.IntegerField(
    initial = '0'
    )
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
    correct = models.IntegerField(
    initial = '0'
    )
    errors = models.IntegerField(
    initial = '0'
    )
    send = models.IntegerField(
    initial = '0'
    )
    earnings = models.CharField(
    initial = '0'
    )

# FUNCTIONS

def count_strategies(group: Group):
    players = group.get_players()
    strategies = [p.strategy for p in players]
    totals = [strategies.count("A"), strategies.count("B"), strategies.count("C")]
    return totals



def set_payoffs(group: Group):
    subsession = group.subsession
    for player in group.get_players():
        payoff_matrix = ([
        subsession.PAYOFF_A,
        subsession.PAYOFF_D,
        subsession.PAYOFF_G],
        [subsession.PAYOFF_B,
        subsession.PAYOFF_E,
        subsession.PAYOFF_H],
        [subsession.PAYOFF_C,
        subsession.PAYOFF_F,
        subsession.PAYOFF_I])
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
    yield ['session', 'participant_code', 'id_in_group', 'payoff', 'choice_history', 'strategy_history', 'payoff_history', 'Game', 'Information', 'Update', 'Rounds', 'Players']
    for p in players:
        yield [p.session.code, p.participant.code, p.id_in_group, p.payoff, p.choice_history, p.strategy_history, p.payoff_history, p.subsession.GAME, p.subsession.INFORMATION, p.subsession.UPDATE, p.subsession.ROUNDS, p.subsession.PLAYERS]


# PAGES
class Introduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        subsession = player.subsession
        subsession.GAME = subsession.session.config['Game']
        subsession.INFORMATION = subsession.session.config['Complete_Information']
        subsession.UPDATE = subsession.session.config['Update']
        subsession.ROUNDS = subsession.session.config['Rounds']
        subsession.PLAYERS = subsession.session.config['Players']
        subsession.OPPONENTS = subsession.PLAYERS - 1
        if subsession.GAME == 1:
            subsession.PAYOFF_A = cu(7)
            subsession.PAYOFF_B = cu(1)
            subsession.PAYOFF_C = cu(7)
            subsession.PAYOFF_D = cu(1)
            subsession.PAYOFF_E = cu(1)
            subsession.PAYOFF_F = cu(1)
            subsession.PAYOFF_G = cu(1)
            subsession.PAYOFF_H = cu(1)
            subsession.PAYOFF_I = cu(9)
        if subsession.GAME == 2:
            subsession.PAYOFF_A = cu(7)
            subsession.PAYOFF_B = cu(3)
            subsession.PAYOFF_C = cu(7)
            subsession.PAYOFF_D = cu(6)
            subsession.PAYOFF_E = cu(8)
            subsession.PAYOFF_F = cu(4)
            subsession.PAYOFF_G = cu(1)
            subsession.PAYOFF_H = cu(7)
            subsession.PAYOFF_I = cu(9)
        if subsession.GAME == 3:
            subsession.PAYOFF_A = cu(7)
            subsession.PAYOFF_B = cu(1)
            subsession.PAYOFF_C = cu(7)
            subsession.PAYOFF_D = cu(6)
            subsession.PAYOFF_E = cu(6)
            subsession.PAYOFF_F = cu(4)
            subsession.PAYOFF_G = cu(1)
            subsession.PAYOFF_H = cu(5)
            subsession.PAYOFF_I = cu(9)
        subsession.EXA = cu(subsession.PAYOFF_C*3)
        subsession.EXB = cu(subsession.PAYOFF_D+2*subsession.PAYOFF_F)
        subsession.EXC = cu(subsession.PAYOFF_G+2*subsession.PAYOFF_I)
        subsession.solution1 = int(subsession.PAYOFF_C)
        subsession.solution12 = int(subsession.PAYOFF_F)
        subsession.solution2 = min(int(subsession.PAYOFF_D), int(subsession.PAYOFF_A))
        subsession.solution3 = max(int(subsession.PAYOFF_B), int(subsession.PAYOFF_C), int(subsession.PAYOFF_E), int(subsession.PAYOFF_F))
        subsession.solution4 = int(2*subsession.PAYOFF_A + 4*subsession.PAYOFF_B + 1*subsession.PAYOFF_C)
        return player.round_number == 1

class Quiz(Page):
    @staticmethod
    def live_method(player: Player, data):
        subsession = player.subsession
        if player.send == 0:
            question = subsession.question1
            player.send = 1
            return {player.id_in_group: dict(
            question = question
            )}
        if 'answer' in data:
            if player.correct == 3:
                if int(data['answer']) == subsession.solution4:
                    feedback = '✓'
                    player.correct += 1
                    player.send = 0
                    is_finished = True
                    return {player.id_in_group: dict(
                    feedback=feedback,
                    is_finished = is_finished
                    )}
                else:
                    player.errors += 1
                    feedback = '✗'
                    question = subsession.question4
            if player.correct == 2:
                if int(data['answer']) == subsession.solution3:
                    feedback = '✓'
                    player.correct += 1
                    question = subsession.question4
                else:
                    player.errors += 1
                    feedback = '✗'
                    question = subsession.question3
            if player.correct == 1:
                if int(data['answer']) == subsession.solution2:
                    feedback = '✓'
                    player.correct += 1
                    question = subsession.question3
                else:
                    player.errors += 1
                    feedback = '✗'
                    question = subsession.question2
            if player.correct == 11:
                if int(data['answer']) == subsession.solution12:
                    feedback = '✓'
                    player.correct = 1
                    question = subsession.question2
                else:
                    player.errors += 1
                    feedback = '✗'
                    question = subsession.question12
            if player.correct == 0:
                if int(data['answer']) == subsession.solution1:
                    feedback = '✓'
                    if subsession.INFORMATION:
                        player.correct = 11
                        question = subsession.question12
                    else:
                        player.correct += 1
                        question = subsession.question2
                else:
                    player.errors += 1
                    feedback = '✗'
                    question = subsession.question1
            return {player.id_in_group: dict(
            feedback=feedback,
            question = question
            )}



class ExperimentWaitPage(WaitPage):
    template_name = 'stepping_stones/ExperimentWaitPage.html'
    def after_all_players_arrive(group: Group):
        group.subsession.now_ms = int((datetime.now(tz=timezone.utc).timestamp()+1) * 1000)



class Experiment(Page):
    @staticmethod
    def live_method(player: Player, data):
        group = player.group
        subsession = player.subsession
        if subsession.send = 0:
            set_payoffs(group)
            if player.strategy == "A":
                play = count_strategies(group)
                play[0] = play[0]-1
            if player.strategy == "B":
                play = count_strategies(group)
                play[1] = play[1]-1
            if player.strategy == "C":
                play = count_strategies(group)
                play[2] = play[2]-1
            message = "<b>Everyone</b> starts the game with <b>A</b> being their last round <font color='GREEN'><b>strategy</b></font>."
            oppA = "".join(["<font color='#0000FF'>A (",str(play[0]),")</font>"])
            oppB = "".join(["<font color='#0000FF'>B (",str(play[1]),")</font>"])
            oppC = "".join(["<font color='#0000FF'>C (",str(play[2]),")</font>"])
            subsession.send = 1
            return {0: dict(
            start=subsession.now_ms,
            message=message,
            strategy=player.strategy,
            play=play,
            oppA=oppA,
            oppB=oppB,
            oppC=oppC
            )}
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
                    if random.random() > subsession.UPDATE:
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
            if player.round >= subsession.ROUNDS:
                finished = "true"
            else:
                finished = "false"
            if (player.change == "true"):
                message = "".join(["Your <font color='GoldenRod'><b>choice</b></font> last round, <font color='GoldenRod'><b>", player.choice, "</b></font>, was randomly <font color='GREEN'><b>accepted</b></font> and your <font color='GREEN'><b>strategy</b></font> was updated. Consequently, your <font color='GREEN'><b>strategy</b></font> for last round is <font color='GREEN'><b>", player.choice, "</b></font>."])
            else:
                message = "".join(["Your <font color='GoldenRod'><b>choice</b></font> last round, <font color='GoldenRod'><b>", player.choice, "</b></font>, was randomly <font color='RED'><b>rejected</b></font> and your <font color='GREEN'><b>strategy</b></font> failed to update. Consequently, your <font color='GREEN'><b>strategy</b></font> for last round is <font color='GREEN'><b>", player.strategy, "</b></font>."])
            #set player.choice to player.strategy
            player.choice = player.strategy
            if (player.strategy == "A"):
                payoff_message = "".join(["Your <font color='Red'><b>payoff</b></font> from the last round: <font color='#0000FF'><b>",str(play[0]),"</b></font>*<font color='FireBrick'><b>",str(subsession.PAYOFF_A),"</b></font> + <font color='#0000FF'><b>",str(play[1]),"</b></font>*<font color='FireBrick'><b>",str(subsession.PAYOFF_B),"</b></font> + <font color='#0000FF'><b>",str(play[2]),"</b></font>*<font color='FireBrick'><b>",str(subsession.PAYOFF_C),"</b></font> = <font color='Red'><b>",str(player.payoff),"</b></font>"])
            if (player.strategy == "B"):
                payoff_message = "".join(["Your <font color='Red'><b>payoff</b></font> from the last round: <font color='#0000FF'><b>",str(play[0]),"</b></font>*<font color='FireBrick'><b>",str(subsession.PAYOFF_D),"</b></font> + <font color='#0000FF'><b>",str(play[1]),"</b></font>*<font color='FireBrick'><b>",str(subsession.PAYOFF_E),"</b></font> + <font color='#0000FF'><b>",str(play[2]),"</b></font>*<font color='FireBrick'><b>",str(subsession.PAYOFF_F),"</b></font> = <font color='Red'><b>",str(player.payoff),"</b></font>"])
            if (player.strategy == "C"):
                payoff_message = "".join(["Your <font color='Red'><b>payoff</b></font> from the last round: <font color='#0000FF'><b>",str(play[0]),"</b></font>*<font color='FireBrick'><b>",str(subsession.PAYOFF_G),"</b></font> + <font color='#0000FF'><b>",str(play[1]),"</b></font>*<font color='FireBrick'><b>",str(subsession.PAYOFF_H),"</b></font> + <font color='#0000FF'><b>",str(play[2]),"</b></font>*<font color='FireBrick'><b>",str(subsession.PAYOFF_I),"</b></font> = <font color='Red'><b>",str(player.payoff),"</b></font>"])
            oppA = "".join(["<font color='#0000FF'>A (",str(play[0]),")</font>"])
            oppB = "".join(["<font color='#0000FF'>B (",str(play[1]),")</font>"])
            oppC = "".join(["<font color='#0000FF'>C (",str(play[2]),")</font>"])
            return {player.id_in_group: dict(
            message=message,
            strategy=player.strategy,
            payoff_message=payoff_message,
            play=play,
            finished=finished,
            oppA=oppA,
            oppB=oppB,
            oppC=oppC
            )}


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        subsession = player.subsession
        payoffrounds = random.sample(range(1,(subsession.ROUNDS+1)), k = 2)
        payoffround1 = payoffrounds[0]
        payoffround2 = payoffrounds[1]
        values = player.payoff_history.split(',')
        payoff1 = values[payoffround1]
        payoff2 = values[payoffround2]
        player.payoff = cu(float(re.sub("[^0-9]", "", payoff1)) + float(re.sub("[^0-9]", "",payoff2)))
        real_world_currency_per_point = float(1/(player.subsession.OPPONENTS))
        variablepay = float(player.payoff) * real_world_currency_per_point
        fixedpay = float(player.session.participation_fee)
        player.earnings = "{:.2f}".format(float(variablepay + fixedpay))
        return dict(
        payoffround1 = payoffround1,
        payoffround2 = payoffround2,
        payoff1 = payoff1,
        payoff2 = payoff2,
        variablepay = "{:.2f}".format(variablepay),
        fixedpay = "{:.2f}".format(fixedpay)
        )



page_sequence = [Introduction, Quiz, ExperimentWaitPage, Experiment, Results]
