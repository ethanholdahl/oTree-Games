from os import environ


SESSION_CONFIGS = [
    dict(
        name='intro_to_gt',
        display_name="Intro to Game Theory",
        app_sequence=['a_guess_two_thirds', 'a_traveler_dilemma', 'a_prisoner_random', 'a_prisoner_repeated', 'a_group_coordination'],
        num_demo_participants=2,
    ),
    dict(
        name='a_guess_two_thirds',
        display_name="Guess 2/3 of the Average",
        app_sequence=['a_guess_two_thirds'],
        num_demo_participants=2,
    ),
    dict(
        name='a_traveler_dilemma',
        display_name="Traveler's Dilemma",
        app_sequence=['a_traveler_dilemma'],
        num_demo_participants=2,
    ),
    dict(
        name='a_prisoner_random',
        display_name="Repeated Prisoner's Dilemma with Random Opponent",
        app_sequence=['a_prisoner_random'],
        num_demo_participants=2,
    ),
    dict(
        name='a_prisoner_repeated',
        display_name="Repeated Prisoner's Dilemma with Same Opponent",
        app_sequence=['a_prisoner_repeated'],
        num_demo_participants=2,
    ),
    dict(
        name='a_group_coordination',
        display_name="Group Coordination Game",
        app_sequence=['a_group_coordination'],
        num_demo_participants=3,
    ),
    dict(
        name='stepping_stones',
        display_name="Stepping Stones",
        app_sequence=['stepping_stones'],
        num_demo_participants=8,
        Game = 1,
        Complete_Information = True,
        Update = .5,
        Rounds = 100,
        Players = 8,
        participation_fee=5.00,
        real_world_currency_per_point=1/14
    ),
    dict(
        name='trust_game',
        display_name="Trust Game with ChatGPT",
        app_sequence=['trust_game'],
        num_demo_participants=2,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    dict(
        name='SS',
        display_name='Stepping Stones Lab'
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '6331451735403'

INSTALLED_APPS = ['otree']
