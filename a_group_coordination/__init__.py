from otree.api import *


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
        choices=[['A', 'Cooperate'], ['B', 'Defect'], ['C', 'C']],
        doc="""This player's decision""",
        widget=widgets.RadioSelect,
    )


# FUNCTIONS
def set_payoffs(group: Group):
    for p in group.get_players():
        set_payoff(p)


def other_player(player: Player):
    return player.get_others_in_group()[0]


def set_payoff(player: Player):
    payoff_matrix = {
        ('A', 'A'): C.PAYOFF_A,
        ('A', 'B'): C.PAYOFF_B,
        ('A', 'C'): C.PAYOFF_C,
        ('B', 'A'): C.PAYOFF_D,
        ('B', 'B'): C.PAYOFF_E,
        ('B', 'C'): C.PAYOFF_F,
        ('C', 'A'): C.PAYOFF_G,
        ('C', 'B'): C.PAYOFF_H,
        ('C', 'C'): C.PAYOFF_I,
    }
    other = other_player(player)
    player.payoff = payoff_matrix[(player.choice, other.choice)]


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
        opponent = other_player(player)
        return dict(
            opponent=opponent,
            same_choice=player.choice == opponent.choice,
            my_decision=player.field_display('choice'),
            opponent_decision=opponent.field_display('choice'),
        )


page_sequence = [Introduction, Decision, ResultsWaitPage, Results]
