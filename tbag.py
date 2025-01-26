from classes import *

dining_hall = Room("Dining Hall", 'You can see a large table in the center of the room')
ballroom = Room('Ballroom', 'There is a large chandelier dangling from the ceiling')
kitchen = Room('Kitchen', 'You are in a small kitchen. There is a wood-burning stove')


dining_hall.add_connected_room(ballroom, "west", True) # True, to assign opposite door
dining_hall.add_connected_room(kitchen, "north", True)

# Create people

john = Person('John')
john.set_dialogue("What are you doing here?")
ballroom.add_person(john)

ball = Item('Ball', 'A spherical object')
ballroom.add_item(ball)

key = dining_hall.lock_direction('west')
kitchen.add_item(key)

rocks = Item('Rocks', 'A satchel of rocks')
dining_hall.add_item(rocks)

gold = Item('Gold', 'A satchel of gold coins')
dining_hall.add_item(gold)

guard = Enemy('Guard', solution_item = gold, description = 'an aggressive looking guard', dialogue = 'None shall pass')
guard.add_item_reponse(gold, 'This is more than a year\'s pay... some shall pass', True, 'Welp, you can\'t take it with you')
dining_hall.add_enemy(guard, 'north')

guard.set_solved_dialogue('Be on your way')
guard.add_fail_item(rocks, 'Now we\'re talking... wait a minute. *The Guard raises his sword* ')

test_list = []
test_list.append(key)
test_list.append(guard)
test_list.append(john)

print(f'Labeled list print {Labeled.display_labeled_list(test_list)}')

#for room in Room.get_all_rooms():
#    room.see_connected_rooms()

class GameLogic:

    game_input_text = "Enter next command (or type 'HELP' to see possible commands)"

    game_running = True

    def start(start_room : Room):
        GameLogic.player = Player()
        GameLogic.current_room = start_room
        GameLogic.run(first_run = True)

    # Run codes. Return 0 == Quit, 1 == Continue, 2 == Invalid Input, 3 == First Run
    # These are returned by player_input

    def run(first_run : bool = False, successful_input : bool = False):
        
        if (first_run):
            print('\n Welcome to the Text Based Adventure Game')
            print('\n You awaken in a mysterious room')
            GameLogic.print_room_description()

        hint = GameLogic.game_input_text if not successful_input else '>>'

        player_input = input(f'{hint} ')
        player_input = str.upper(player_input)

        input_result = GameLogic.handle_input(player_input)

        if (input_result == 0): # Quit command sent
            return
        elif (input_result == 1): # Input was successful
            GameLogic.run(successful_input = True) # Run without re-hinting
        elif (input_result == 2):
            GameLogic.run(successful_input = False) # Run with hinting
        else:
            GameLogic.game_over(); 

    
    def handle_input(input : str) -> int:
        
        try: # I don't want to resolve each individual potential error case

            if input == 'QUIT':
                print(f'Quitting...')
                return 0

            if input == 'HELP':
                GameLogic.print_options()
                return 1
            
            if input == 'INVENTORY':
                print(f'\nYou are carrying {GameLogic.player.get_inventory()} \n')
                return 1
            
            if input == 'LOOK':
                GameLogic.print_room_description()
                return 1
            
            else:
                split_input = str.split(input)

                if split_input[0] == 'GO':
                    return GameLogic.go_in_direction(split_input[1])
                
                elif split_input[0] == 'PICKUP':
                    return GameLogic.pickup_item(split_input[1])
                
                elif split_input[0] == 'INSPECT':
                    return GameLogic.inspect_item(split_input[1])
                
                elif split_input[0] == 'USE':
                    try:
                        if split_input[2] == 'ON': # i.e. 'USE item ON obstacle' entered
                            return GameLogic.start_use_item(split_input[1], split_input[3])
                    except:
                        return GameLogic.start_use_item(split_input[1])
                
                elif split_input[0] == 'TALK':
                    if split_input[1] == 'TO':
                        return GameLogic.talk_to_person(split_input[2])
                    
                elif split_input[0] == 'CONFRONT' or split_input[0] == 'FIGHT':
                    try:
                        if split_input[2] == 'WITH': # i.e. 'CONFRONT enemy WITH item'
                            return GameLogic.confront_enemy(split_input[1], split_input[3])
                    except:
                        return GameLogic.confront_enemy(split_input[1])


            print(f'Invalid input')
            return 2

        except:
            print(f'Invalid input')
            return 2

    def print_options():
        
        options_list = []

        options_list.append('LOOK')

        # DIRECTIONS
        for direction in GameLogic.current_room.get_valid_directions():
            options_list.append(f'GO {str.upper(direction)}')

        # ITEMS
        for item in GameLogic.current_room.get_items():
            options_list.append(f'PICKUP {str.upper(f'{item}')}')

        for item in GameLogic.player.get_items():
            options_list.append(f'INSPECT {str.upper(f'{item}')}')
        
        for item in GameLogic.player.get_items():
            options_list.append(f'USE {str.upper(f'{item}')}')

        for person in GameLogic.current_room.get_people_in_room():
            options_list.append(f'TALK TO {str.upper(f'{person.get_name()}')}')
        
        for enemy in GameLogic.current_room.get_enemies():
            options_list.append(f'CONFRONT {str.upper(enemy.get_name())}')


        options_list.append('INVENTORY')

        options_list.append('QUIT')

        print(f'Options: {options_list}')


    def go_in_direction(direction : str):

        direction = str.lower(direction)

        can_go_in_direction, message = GameLogic.current_room.can_go_in_direction(direction)

        print(f'\n{message}')

        if can_go_in_direction:
            GameLogic.current_room = GameLogic.current_room.get_room_in_direction(direction)
            GameLogic.print_room_description()
            return 1
        else:
            return 2

    def pickup_item(item_name : str):

        item_name = str.lower(item_name)

        if not (item := GameLogic.current_room.get_item(item_name)) == None:
            print(f"Picked up {item.get_name()}")
            GameLogic.current_room.remove_item(item)
            GameLogic.player.add_item(item)
            return 1
        else:
            print("No such item")
            return 2
    
    def inspect_item(item_name : str):

        item_name = str.lower(item_name)

        if not (item := GameLogic.player.get_item(item_name)) == None:
            print(f'\n{item.get_description()}')
            return 1
        else:
            print("You are not carrying that item")
            return 2
        
    def start_use_item(item_name : str, obstacle_name = None) -> int:

        '''
        Returns int value: 1 (Valid Item), 2 (Invalid Item)
        '''

        item_name = str.lower(item_name)

        if not (item := GameLogic.player.get_item(item_name)) == None:

            if not obstacle_name == None:
                return GameLogic._use_item(item, obstacle_name)
            else:
                print(f"Use {item.get_name()} on: ")
                return GameLogic._use_item(item, input(">> "))
        else:
            print("You are not carrying that item")
            return 2
    
    def _use_item(item : Item, obstacle_name : str) -> int: # State

        '''
        Returns int value: 1 (Valid Obstacle), 2 (Invalid Obstacle)
        '''

        obstacle_name = str.lower(obstacle_name)

        for room_obstacle in GameLogic.current_room.get_obstacles():

            if room_obstacle == None:
                continue

            # Handle enemy fail
            if type(room_obstacle) == Enemy:
                fail_check = room_obstacle.check_fail(item)

                if fail_check[0] == True:
                    print (fail_check[1])
                    return 3

            if obstacle_name == str.lower(room_obstacle.get_name()):
                item_works, message, item_destroyed, destroy_message \
                      = room_obstacle.check_item(item)

                if item_works:
                    GameLogic.current_room.remove_obstacle(room_obstacle)
                    room_obstacle.set_solved()

                print(message)

                if item_destroyed:
                    GameLogic.player.remove_item(item)
                    print(destroy_message)

                return 1
        
        print(f'{obstacle_name} is not a valid obstacle name')
        return 2
    
    def talk_to_person(person_name : str) -> int: # state

        '''
        Returns int value: 1 (Valid Person), 2 (Invalid Person)
        '''

        person_name = str.lower(person_name)

        for person in GameLogic.current_room.get_people_in_room():

            if person_name == str.lower( person.get_name() ):
                print(person.get_dialogue())
                return 1
        
        print('Invalid person name')
        return 2
    
    def confront_enemy(enemy_name : str, item_name : str = None):

        # Re-using use item implementation
        enemy_name_valid = False

        for enemy in GameLogic.current_room.get_enemies():
            if str.upper (enemy.get_name()) == enemy_name:
                enemy_name_valid = True

        if not enemy_name_valid:
            print("Invalid enemy name")
            return 2

        if item_name == None:
            print(f"Confront {enemy_name} with: ")
            return GameLogic.start_use_item(input(">> "), enemy_name)
        else:
            return GameLogic.start_use_item(item_name, enemy_name)


    def print_room_description():
        print('\n', GameLogic.current_room.get_full_description(), '\n')
    
    def game_over():
        print("\n GAME OVER! \n")


GameLogic.start(start_room = dining_hall)


