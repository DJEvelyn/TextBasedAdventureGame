from abc import ABC, abstractmethod

# ABSTRACT CLASS for neatness. Person, Item and Room have name & description
class Labeled(ABC):

    @abstractmethod
    def __init__(self, name : str, description = None):
        self.labeled_init(name, description)

    """ * """
    def labeled_init(self, name : str, description = None):
        self.set_name(name)
        self.set_description(description)
    
    """
    Work around for multi-inheritence
    Can't just call super().__init__()
    """

    def __str__(self):
        return self.get_name()

    # SETTERS
    def set_name(self, name : str):
        self.name = name
    
    def set_description(self, description : str):
        self.description = description
    
    # GETTERS
    def get_name(self) -> str:
        return self.name[:] # Cloned
    
    def get_description(self) -> str:
        return self.description[:] # Cloned
    
    def display_labeled_list(list : list) -> str:

        items_message = ''

        for i in range(0, length := len(list)):
            current_label = list[i]

            if (i + 1 >= length):
                items_message = f'{items_message} {current_label}.'
            else:
                items_message = f'{items_message} {current_label},'
        
        return f'{items_message}'



class Item(Labeled):

    def __init__(self, name : str, description = None):
        self.labeled_init(name, description)
        
    # GETTERS
    def inspect_item(self):
        if self.description == None:
            print("This item has no description")
        else:
            print(f'{self.description}')

    def __str__(self):
        return self.name

# ABSTRACT CLASS for neatness. Person and Room share item logic 
class ItemHolder(ABC):

    @abstractmethod
    def __init__(self):
        self.item_holder_init()

    """ * """
    def item_holder_init(self):
        self.inventory = []
    
    """
    Work around for multi-inheritence
    Can't just call super().__init__()
    """
    
    def add_item(self, item : Item):
        self.inventory.append(item)
    
    def remove_item(self, item : Item):
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        else:
            return False
        
    def get_items(self):
        return self.inventory[:] # Clone
    
    def get_item_count(self):
        return len(self.get_items())

    def get_item(self, item_name : str) -> Item: # Retrieve item by name
        
        for item in self.get_items():
            if str.lower(item.get_name()) == item_name:
                return item
        
        return None
        
    def get_inventory(self) -> str:
        # Format -> 3 items: Item1, Item2 and Item3.
        item_count = self.get_item_count()

        if item_count == 0:
            return 'no items.'
        
        item_text = 'items' if item_count > 1 else 'item'

        return f'{item_count} {item_text}: {Labeled.display_labeled_list(self.get_items())}'

class Person(Labeled, ItemHolder):

    default_response = "doesn't want to talk"

    def __init__(self, name : str, dialogue = None):
        self.person_init(name, dialogue)
    
    def person_init(self, name : str, dialogue = None): # for multi-inheritence
        self.labeled_init(name)
        self.item_holder_init()
        self.dialogue = dialogue
    
    def set_dialogue(self, given_dialogue):
        self.dialogue = given_dialogue

    def get_dialogue(self) -> str:
        if self.dialogue == None:
            return f'{self.get_name()} {Person.default_response}'
        else:
            return f'{self.get_name()}: "{self.dialogue[:]}"'
        
    def __str__(self):
        return self.get_name(); 
    
class Player(Person):

    def __init__(self):
        super().__init__('Player')

class Ally(Person):

    def __init__(self, name : str, gift_item : Item):
        
        if gift_item == None:
            print('Allies must have a gift item')
            return 

        super().__init__(name)
        self.gift_item = gift_item
    
    def set_gave_item_dialogue(self, gave_item_dialogue : str):
        self.gave_item_dialogue = gave_item_dialogue

    
    def get_gift_item(self):
        
        if self.gift_item == None:
            return None
        
        outbound_gift = self.gift_item
        self.gift_item = None
        
        if not self.gave_item_dialogue == None:
            self.set_dialogue(self.gave_item_dialogue)

        return outbound_gift
        



class Obstacle(Labeled):

    DEFAULT_RESPONSE = "did not work"

    def __init__(self, solution_item : Item, name : str, description = None):
        self.obstacle_init(solution_item, name, description)

    def obstacle_init(self, solution_item : Item, name : str, description = None): # For multi-inheritence
        self.labeled_init(name, description)
        self.solved_state = False
        self.solution_item = solution_item
        self.item_responses = {}
        self.item_destroyed = {}
    
    # Setters
    def add_item_response(self, item : Item, response : str, destroys_item : bool = False, destroy_message : str = None):
        self.item_responses[item] = response
        
        if destroys_item:
            self.item_destroyed[item] = f'{item.get_name()} was destroyed' if destroy_message == None else destroy_message; 

    # Getters
    def _get_item_response(self, item : Item):
        try:
            return self.item_responses[item]
        except:
            return f'{item.get_name()} {Obstacle.DEFAULT_RESPONSE}'
    
    def _get_destroy_item_response(self, item : Item):
        if item in self.item_destroyed.keys():
            return True, self.item_destroyed[item]
        else:
            return False, "[Item was not destroyed]"

    def check_item(self, item : Item) -> tuple[bool, str, bool, str]: # True/False of item working, + message
        destroy_tuple = self._get_destroy_item_response(item)
        
        return (item == self.solution_item), self._get_item_response(item), \
        destroy_tuple[0], destroy_tuple[1]

    def set_solved(self):
        self.solved_state = True
        



class Enemy(Person, Obstacle):

    def __init__(self, name : str, solution_item : Item, dialogue = None, description = None, solved_dialogue = None):
        self.person_init(name, dialogue)
        self.obstacle_init(solution_item, name, description)

        self.fail_items = {}
        self.solved_dialogue = solved_dialogue

    def set_solved_dialogue(self, solved_dialogue : str):
        self.solved_dialogue = solved_dialogue

    def add_fail_item(self, item : Item, message : str):

        if item == self.solution_item:
            print('Invalid. Fail item cannot be solution item')
            return

        self.fail_items[item] = message
    
    def check_fail(self, item : Item) -> tuple[bool, str]: # Fail status and fail message

        if (item in self.fail_items.keys()):
            return True, self.fail_items[item]
        else:
            return False, "[Not a fail item]"
        
    def set_solved(self):
        self.solved_state = True

        if self.solved_dialogue != None:
            self.set_dialogue(self.solved_dialogue)


class Room(Labeled, ItemHolder):

    all_rooms = []

    directions = ['north', 'east', 'south', 'west']

    def __init__(self, room_name, description):
        
        self.labeled_init(room_name, description)
        self.item_holder_init()
        
        self.connected_rooms = {}

        self.obstacles = {}
        for direction in Room.directions:
            self.obstacles[direction] = None

        self.people = []

        Room.all_rooms.append(self) # Keep track of all room objects in Room class

    # SETTERS
    def add_connected_room(self, room, direction, two_way = False):

        if direction == None:
            return
        
        direction = str.lower(direction)

        if direction in self.connected_rooms.keys(): # Already allocated
            return
        else:
            self.connected_rooms[direction] = room

            if two_way == True:
                room.add_connected_room( self, Room.get_opposite_direction(direction), False)

    def add_person(self, person : Person):
        
        # Check that person isn't in any other room
        
        for room in Room.all_rooms:
            for room_person in room.get_people_in_room():
                if person == room_person:
                    return # Exit method. This would be a clone.
        
        self.people.append(person)
    
    def add_obstacle(self, obstacle : Obstacle, *directions : str): # Only one obstacle per direction
        for direction in directions:
            self.obstacles[direction] = obstacle

    def remove_obstacle(self, obstacle : Obstacle):
        for entry in self.obstacles.items():
            if entry[1] == obstacle:
                obstacle_direction = entry[0]
        
        self.obstacles[obstacle_direction] = None
            

    def add_enemy(self, enemy : Enemy, *directions : str):
        self.add_obstacle(enemy, *directions)
        self.add_person(enemy)


    # GETTERS

    def get_full_description(self) -> str: # Multi-line. Room, People and Items
        
        line_one = self.get_description()
        line_two = self.get_people_in_room_text()
        line_three = f'The room has {self.get_inventory()}'

        return f'{line_one} \n{line_two} \n{line_three}'

    def get_people_in_room(self) -> list[Person]:
        return self.people[:] # Cloned list

    def get_people_in_room_text(self):
        people_count = len(self.people)

        if people_count > 0:
            count_text = f'You can see {people_count} people' if  people_count > 1 else f'You can see {people_count} person'
            return f'{count_text}: { Labeled.display_labeled_list(self.get_people_in_room()) }'
        else:
            return f'There is nobody in the room'

    def see_connected_rooms(self):

        print (f'Room {self} has a door to:')

        for connected_room in self.connected_rooms.items():
            print(f'{connected_room[1]} in the {connected_room[0]}')

        print('\n')
    
    def get_valid_directions(self):
        return self.connected_rooms.keys()
    
    def can_go_in_direction(self, direction : str) -> tuple[bool, str]: # tuple[can_go, message] 
        
        if self.get_room_in_direction(direction) == None:
            return [False, 'There is no door in that direction']
        
        if (obstacle := self.obstacles[direction]) == None:
            return [True, ""]
        else:
            return [False, f'The {direction} door is blocked by {obstacle.get_description()} - [{obstacle.get_name()}]']
            
    def get_room_in_direction(self, direction):
        if direction in self.connected_rooms.keys():
            return self.connected_rooms[direction]
        else:
            return None
    
    def get_obstacle_in_direction(self, direction):
        return self.obstacles[direction]
        
    def lock_direction(self, direction : str) -> Item:
        
        # Check if there is a room in that direction
        if ( given_room := self.get_room_in_direction(direction) ) == None:
            print(f"No room in that direction for {self.get_name()}")
            return
        else:
            # Create key
            key_name = f'Key'
            key_description = f'A key for the {self.get_name()}\'s {direction} door (to {given_room.get_name()})'
            key = Item(key_name, key_description)

            # Create lock
            lock = Lock(key)

            self.add_obstacle(lock, direction)

            return key 
    
    def get_obstacles(self) -> list[Obstacle]:
        return self.obstacles.values()
    
    def get_enemies(self) -> list[Enemy]:
        return [x for x in self.get_obstacles() if type(x) == Enemy]


    # STATIC METHODS

    def get_all_rooms():
        return Room.all_rooms[:]
    
    def get_opposite_direction(direction):
        if not direction in Room.directions:
            return None
        else:
            current_direction_index = Room.directions.index(direction)
            opposite_direction_index = (current_direction_index + 2) % len(Room.directions)
            return Room.directions[opposite_direction_index]
    
class Lock(Obstacle):

    def __init__(self, key : Item):
        super().__init__(key, "Door", "with a lock")
        self.add_item_response(key, f'The {key.get_name()} works', True, 'You leave the key in the door')



    
    



