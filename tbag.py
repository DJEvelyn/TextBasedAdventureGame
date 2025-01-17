from classes import *

dining_hall = Room("Dining Hall", 'You can see a large table in the center of the room')
ballroom = Room('Ballroom', 'There is a large chandelier dangling from the ceiling')
kitchen = Room('Kitchen', 'You are in a small kitchen. There is a wood-burning stove')


dining_hall.add_connected_room(ballroom, "west", True) # True, to assign opposite door
dining_hall.add_connected_room(kitchen, "north", True)

# Create people

john = Person('John')
ballroom.add_person(john)

#for room in Room.get_all_rooms():
#    room.see_connected_rooms()

class GameLogic:

    game_input_text = "Enter next command (or type 'HELP' to see possible commands)"

    game_running = True

    def start(start_room : Room):
        GameLogic.current_room = start_room
        GameLogic.run()

    def run():

        print(GameLogic.current_room.get_description())
        
        player_input = input(f'{GameLogic.game_input_text} ')
        player_input = str.upper(player_input)

        input_result = GameLogic.handle_input(player_input)

        if (input_result == False):
            return
        else:
            GameLogic.run()

    
    def handle_input(input : str):
        
        if input == 'QUIT':
            print(f'Quitting...')
            return False

        if input == 'HELP':
            GameLogic.print_options()
            return True
        
        else:
            split_input = str.split(input)

            if split_input[0] == 'GO':
                return GameLogic.go_in_direction(split_input[1])

        print(f'Invalid input')
        return True

    def print_options():
        
        direction_list = []

        for direction in GameLogic.current_room.get_valid_directions():
            direction_list.append(f'GO {str.upper(direction)}')
        
        direction_list.append('QUIT')

        print(f'Options: {direction_list}')


    def go_in_direction(direction : str):

        direction = str.lower(direction)

        if (room := GameLogic.current_room.get_room_in_direction(direction) ):
            print(f'You went through the door to the {direction}')
            GameLogic.current_room = room
            return True
        else:
            print("There is no door in that direction")

GameLogic.start(start_room = dining_hall)


