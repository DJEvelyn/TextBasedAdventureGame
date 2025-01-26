from classes import *

# ROOMS

entrance_hall = Room("Entrance Hall", "A grand foyer with ornate decorations and an exit to the south")
dining_hall = Room("Dining Hall", "A large room with a long dining table set for a feast.")
ballroom = Room("Ballroom", "A grand room with crystal chandeliers and polished floors.")
kitchen = Room("Kitchen", "Well-equipped with a variety of cooking tools.")
library = Room("Library", 'A cozy room filled with bookshelves and ... a high window.')
office = Room("Office", 'A mystical chamber with shimmering scrolls and a crystal desk radiating an ethereal glow.')
outdoors = Room("Outdoors", " ")


entrance_hall.add_connected_room(dining_hall, 'north', True)
dining_hall.add_connected_room(kitchen, 'north', True)
ballroom.add_connected_room(dining_hall, 'east', True)
library.add_connected_room(dining_hall, 'west', True)
outdoors.add_connected_room(entrance_hall, 'north', True)
office.add_connected_room(library, 'west', True)


# ITEMS

key = entrance_hall.lock_direction('south')
gold = Item('Gold', 'A small satchel of gold coins. A decent amount for a bribe.')
ball = Item('Ball', 'A spherical object. Perfectly so, on second glance.')
knife = Item('Knife', 'A dull butterknife.')
book = Item('Book', 'A book covered in dust. It hasn\'t been read in years')


# Allies
stranger = Ally('Stranger', gold)
stranger.set_dialogue('You\'ll be needing this')
stranger.set_gave_item_dialogue('Some are more loyal to gold')
stranger.set_description('A mysterious figure')

# Enemies
chef = Enemy('Chef', gold, 'Nobody gets into my kitchen', 'a chef in full-attire', 'Some people get into my kitchen')
chef.set_description('A chef in full-attire')
chef.add_item_response(gold, 'You\'re right, I am underpaid. *You hand the satchel to the chef*', True, '*The chef steps aside*')
chef.add_item_response(ball, 'I don\'t have time for games')
chef.add_item_response(book, 'It doesn\'t look like a recipe book to me')

guard = Enemy('Guard', book, 'It is my duty to guard the library', 'a fearsome looking guard', 'Please take the book to the library')
guard.add_item_response(book, 'Ah, you must have business here. *The guard steps aside*')
guard.add_fail_item(ball, 'You mock me!? *The guard raises his sword *')
guard.add_fail_item(knife, 'Ah! Then it is a duel. *The guard raises his sword*')
guard.add_item_response(gold, 'You cannot bribe a guard of my standing')

librarian = Enemy('Librarian', book, 'Now where has it gone...', 'a librarian, slender and wearing spectacles', 'I appreciate the help. Please, see yourself out.')
librarian.add_item_response(book, 'Just what I was looking for', True, '*The librarian takes the book*')
librarian.add_item_response(knife, 'Is that supposed to be intimidating?')

# Assign people

ballroom.add_person(stranger)
dining_hall.add_enemy(chef, 'north')
library.add_enemy(librarian, 'east')
dining_hall.add_enemy(guard, 'east')


# Assign items

office.add_item(key)
ballroom.add_item(ball)
kitchen.add_item(knife)
kitchen.add_item(book)



class GameLogic:

    game_input_text = "Enter next command (or type 'HELP' to see possible commands)"

    game_running = True

    def start(start_room : Room, target_room : Room):
        GameLogic.player = Player()
        GameLogic.current_room = start_room
        GameLogic.target_room = target_room
        GameLogic.run(first_run = True)

    # Run codes. Return 0 == Quit, 1 == Continue, 2 == Invalid Input, 3 == First Run
    # These are returned by player_input

    def run(first_run : bool = False, successful_input : bool = False):
        
        if (first_run):
            print('\n Welcome to the Text Based Adventure Game')
            print('\n You awaken in a mysterious room')
            GameLogic.print_room_description()

        if GameLogic.current_room == GameLogic.target_room:
            GameLogic.game_won()
            return

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
                
                elif split_input[0] == 'GIVE':
                    try:
                        if split_input[2] == 'TO': # i.e. 'GIVE item TO obstacle' entered
                            return GameLogic.start_use_item(split_input[1], split_input[3])
                    except:
                        return GameLogic.start_use_item(split_input[1], give_command = True)
                
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
        
    def start_use_item(item_name : str, obstacle_name = None, give_command = False) -> int:

        '''
        Returns int value: 1 (Valid Item), 2 (Invalid Item)
        '''

        item_name = str.lower(item_name)

        if not (item := GameLogic.player.get_item(item_name)) == None:

            if not obstacle_name == None:
                return GameLogic._use_item(item, obstacle_name)
            else:

                message = f'Use {item.get_name()} on: ' if not give_command else f'Give {item.get_name()} to: '
                print(message)
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

            if not obstacle_name == str.lower(room_obstacle.get_name()):
                continue

            # Handle enemy fail
            if type(room_obstacle) == Enemy:
                fail_check = room_obstacle.check_fail(item)

                if fail_check[0] == True:
                    print (fail_check[1])
                    return 3

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
            
        for person in GameLogic.current_room.get_people_in_room():
            if str.lower(person.get_name()) == obstacle_name:
                print(f'{str.upper(obstacle_name)} is not an obstacle')
                return 2
        
        print(f'There is not obstacle called {obstacle_name}')
        return 2
    
    def talk_to_person(person_name : str) -> int: # state

        '''
        Returns int value: 1 (Valid Person), 2 (Invalid Person)
        '''

        person_name = str.lower(person_name)

        for person in GameLogic.current_room.get_people_in_room():

            if person_name == str.lower( person.get_name() ):
                print(person.get_dialogue())

                if type(person) == Ally:
                    if not (gift_item := person.get_gift_item()) == None:
                        print(f'Received {gift_item.get_name()} from {person.get_name()}')
                        GameLogic.player.add_item(gift_item)

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
    
    def game_won():
        print('\nYou have made it outside!')
        GameLogic.game_over()

    def game_over():
        print("\n GAME OVER! \n")


GameLogic.start(start_room = entrance_hall, target_room = outdoors)


