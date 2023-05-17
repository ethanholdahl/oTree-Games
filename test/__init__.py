from otree.api import *

doc = """
Test
"""


class C(BaseConstants):
    NAME_IN_URL = 'test'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    pass



class Minimal(Page):
    pass




page_sequence = [Minimal]
