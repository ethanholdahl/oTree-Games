from otree.api import *
import numpy as np

doc = """
This is a repeated "Prisoner's Dilemma" against the same opponent each round.
Two players are asked separately whether they want to cooperate or defect.
Their choices directly determine the payoffs.
"""


class C(BaseConstants):
    NAME_IN_URL = 'a_group_coordination'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 5
    INSTRUCTIONS_TEMPLATE = 'a_group_coordination/instructions.html'
    PAYOFF_A = cu(10)
    PAYOFF_B = cu(0)
    PAYOFF_C = cu(0)
    PAYOFF_D = cu(0)
    PAYOFF_E = cu(10)
    PAYOFF_F = cu(0)
    PAYOFF_G = cu(0)
    PAYOFF_H = cu(0)
    PAYOFF_I = cu(10)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    choice = models.CharField(
        choices=[['A', 'A'], ['B', 'B'], ['C', 'C']],
        doc="""This player's decision""",
        widget=widgets.RadioSelect,
    )


# FUNCTIONS

def count_choices(group: Group):
    players = group.get_players()
    choices = [p.choice for p in players]
    totals = [choices.count("A"), choices.count("B"), choices.count("C")]
    print(totals)
    return totals



def set_payoffs(group: Group):
    for player in group.get_players():
        payoff_matrix = ([
        C.PAYOFF_A,
        C.PAYOFF_B,
        C.PAYOFF_C],
        [C.PAYOFF_D,
        C.PAYOFF_E,
        C.PAYOFF_F],
        [C.PAYOFF_G,
        C.PAYOFF_H,
        C.PAYOFF_I])
        if player.choice == "A":
            play = count_choices(group)
            play[0] = play[0]-1
            payoff = np.dot(play,payoff_matrix)[0]
        if player.choice == "B":
            play = count_choices(group)
            play[1] = play[1]-1
            payoff = np.dot(play,payoff_matrix)[1]
        if player.choice == "C":
            play = count_choices(group)
            play[2] = play[2]-1
            payoff = np.dot(play,payoff_matrix)[2]
        player.payoff = payoff
        print(player.payoff)
        set_payoff(player)



def other_player(player: Player):
    return player.get_others_in_group()[0]


def set_payoff(player: Player):
    other = other_player(player)
    #player.payoff = payoff_matrix[(player.choice, other.choice)]


# PAGES
class Introduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Decision(Page):
    form_model = 'player'
    form_fields = ['choice']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        for player in group.get_players():
            if player.choice == "A":
                play = count_choices(group)
                play[0] = play[0]-1
            if player.choice == "B":
                play = count_choices(group)
                play[1] = play[1]-1
            if player.choice == "C":
                play = count_choices(group)
                play[2] = play[2]-1
        return dict(
            picked_A=play[0],
            picked_B=play[1],
            picked_C=play[2],
            my_decision=player.field_display('choice')
        )


page_sequence = [Introduction, Decision, ResultsWaitPage, Results]
