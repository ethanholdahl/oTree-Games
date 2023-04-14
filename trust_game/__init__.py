from otree.api import *
import openai
import Keys

openai.api_key = Keys.openai

doc = """
For oTree beginners, it would be simpler to implement this as a discrete-time game
by using multiple rounds, e.g. 10 rounds, where in each round both players can make a new proposal,
or accept the value from the previous round.

However, the discrete-time version has more limitations
(fixed communication structure, limited number of iterations).

Also, the continuous-time version works smoother & faster,
and is less resource-intensive since it all takes place in 1 page.
"""


class C(BaseConstants):
    NAME_IN_URL = 'trust_game'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    PLAYERA_ROLE = 'Player A'
    PLAYERB_ROLE = 'Player B'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    outcome = models.LongStringField()


class Player(BasePlayer):
    message_sent_to_AI = models.LongStringField()
    message_sent = models.LongStringField()
    message_AI_assistant = models.LongStringField()
    message_method = models.LongStringField()
    amount_accepted = models.IntegerField()
    choice = models.LongStringField()
    earnings = models.IntegerField()



#FUNCTIONS



def reword_player_B_message(message):
    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=[{"role":"system", "content": "There is a 2-player game occurring between the user and another player, Player A. Player A makes the first decision and must choose to play either 'In' or 'Out'. If Player A chooses 'Out' then the game ends and both the user and Player A get a payoff of 5. If Player A chooses 'In', then the user must decide between playing either 'L' or 'R'. If the user chooses 'L' then the game ends and both Player A and the user get a payoff 10. If the user chooses R, then the game ends and the user gets a payoff of 14 and Player A gets a payoff of 0. The user can send a message to Player A before Player A decideds to play 'In' or 'Out'. You are an assistant to the user. Your job is to help the user write a clear message to Player A. You should analyze the message and make any necessary suggestions to help make the user's message to Player A more clear and convincing. You should also end your reply to the user by revising the user's message to Player A while making it as clear and convincing as possible. You should prepend the revised message with 'Click the button below to send the following message to Player A:'"},
        {"role":"user", "content": message}]
    )
    assistantB_message = completion.choices[0].message.content
    print(assistantB_message)
    return(assistantB_message)

def interpret_message_for_player_A(message):
    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=[{"role":"system", "content": "There is a 2-player game. Player A moves first. Player A can choose Out or In. If they choose Out then both players get a payoff of 5. If they choose In, it is player B's turn to move. Player B can choose either L or R. If player B chooses L both players get 10. If player B chooses R, they get a payoff of 14 and player A gets a payoff of 0. Player B can send a message to player A before the game starts. You are an assistant to player A. Your job is to interpret the message sent by player B to help player A make their decision."},
        {"role":"user", "content": "Player B said: " + message}]
    )
    assistantA_message = completion.choices[0].message.content
    return(assistantA_message)

class Experiment(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(other_role=player.get_others_in_group()[0].role)

    @staticmethod
    def js_vars(player: Player):
        return dict(my_id=player.id_in_group)

    @staticmethod
    def live_method(player: Player, data):

        group = player.group
        [other] = player.get_others_in_group()

        if 'message' in data:
            message = data['message']
            if data['type'] == 'BtoAI':
                print(message)
                player.message_sent_to_AI = message
                player.message_AI_assistant = reword_player_B_message(message)
                messageAIB = player.message_AI_assistant
                return {2: dict(messageAIB = messageAIB)}
            if data['type'] == 'BtoA':
                player.message_sent = message
                player.message_method = "Own"
                messageToA = message
                messageInterpretA = interpret_message_for_player_A(message)
                return {1: dict(messageToA = messageToA, messageInterpretA = messageInterpretA)}
            if data['type'] == 'AItoA':
                print(message)
                index = message.find('Click the button below to send the following message to Player A:')
                print(index)
                #Incase the message key isn't found:
                if index != -1:
                    index = index+65
                else:
                    index = 0
                aimessage = message[index:]
                print(aimessage)
                player.message_sent = aimessage
                player.message_method = "AI"
                messageToA = aimessage
                messageInterpretA = interpret_message_for_player_A(aimessage)
                return {1: dict(messageToA = messageToA, messageInterpretA = messageInterpretA)}
        if 'choice' in data:
            choice = data['choice']
            player.choice = choice
            print(player.choice)
            if other.field_maybe_none('choice') != None:
                if player.id_in_group == 1:
                    choiceA = player.choice
                    choiceB = other.choice
                else:
                    choiceA = other.choice
                    choiceB = player.choice
                if choiceA == "Out":
                    group.outcome = "Out"
                else:
                    group.outcome = choiceB
                return {0: dict(finished = "finished")}


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        outcome = player.group.outcome
        pathA = "https://ethanholdahl.com/assets/images/trust-game-AI/Player-A-Game-Tree-" + outcome + ".jpg"
        pathB = "https://ethanholdahl.com/assets/images/trust-game-AI/Player-B-Game-Tree-" + outcome + ".jpg"
        if outcome == "R":
            if player.id_in_group == 1:
                player.earnings = 0
            else:
                player.earnings = 14
            messageA = "The game is over. You selected 'In' and Player B selected 'R'. As result, you earned 0 points."
            messageB = "The game is over. Player A selected 'In' and you selected 'R'. As result, you earned 14 points."
        elif outcome == "L":
            player.earnings = 10
            messageA = "The game is over. You selected 'In' and Player B selected 'R'. As result, you earned 10 points."
            messageB = "The game is over. Player A selected 'In' and you selected 'R'. As result, you earned 10 points."
        else:
            player.earnings = 5
            messageA = "The game is over. You selected 'Out'. As result, you earned 5 points."
            messageB = "The game is over. Player A selected 'Out'. As result, you earned 5 points."

        return dict(
        gameTreePathA = pathA,
        gameTreePathB = pathB,
        messageA = messageA,
        messageB = messageB
        )


page_sequence = [Experiment, Results]
