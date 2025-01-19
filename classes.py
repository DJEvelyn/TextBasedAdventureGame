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

        item_iterator = iter(self.get_items())

        items_message = ''

        while True: # has next
            try:
                current_item = next(item_iterator)
                items_message = f'{items_message} {current_item}'
            except: # End of iteration
                items_message = f'{items_message}.' # Add full stop
                break
                
            items_message = f'{items_message},' # On to the next, add comma.

        return f'{item_count} items: {items_message}'


class Person(Labeled, ItemHolder):

    def __init__(self, name : str):
        self.labeled_init(name)
        self.item_holder_init()

class Player(Person):

    def __init__(self):
        super().__init__('Player')

class Room(Labeled, ItemHolder):

    all_rooms = []

    directions = ['north', 'east', 'south', 'west']

    def __init__(self, room_name, description):
        
        self.labeled_init(room_name, description)
        self.item_holder_init()
        
        self.connected_rooms = {}
        self.locked_directions = set()
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
        

    # GETTERS

    def get_full_description(self) -> str: # Multi-line. Room, People and Items
        
        line_one = self.get_description()
        line_two = self.get_people_in_room_text()
        line_three = f'The room has {self.get_inventory()}'

        return f'{line_one} \n{line_two} \n{line_three}'

    def get_people_in_room(self):
        return self.people[:] # Cloned list

    def get_people_in_room_text(self):
        people_count = len(self.people)

        if people_count > 0:
            count_text = f'You can see {people_count} people' if  people_count > 1 else f'You can see {people_count} person'
            return f'{count_text}'
        else:
            return f'There is nobody in the room'

    def see_connected_rooms(self):

        print (f'Room {self} has a door to:')

        for connected_room in self.connected_rooms.items():
            print(f'{connected_room[1]} in the {connected_room[0]}')

        print('\n')
    
    def get_valid_directions(self):
        return self.connected_rooms.keys()
    
    def get_room_in_direction(self, direction):
        if direction in self.connected_rooms.keys():
            return self.connected_rooms[direction]
        else:
            return None
        
    def lock_direction(self, direction : str) -> Item:
        
        # Check if there is a room in that direction
        if ( given_room := self.get_room_in_direction(direction) ) == None:
            print(f"No room in that direction for {self.get_name()}")
            return
        else:
            self.locked_directions.add(direction)
            key_name = f'{self.get_name()} key'
            key_description = f'A key for the {self.get_name()}\'s {direction} door (to {given_room.get_name()})'
            key = Key(key_name, key_description)
            key.assign_key(self, direction)
            return key 

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
    

class Key(Item):

    def __init__(self, name : str, description : str):
        super().__init__(name, description)

    def assign_key(self, room : Room, direction : str):
        self.key_room = room
        self.key_room_direction = direction
    
    def check_key(self, room : Room, direction : str):
        return (self.key_room == room) and (self.key_room_direction == direction)
    






    
    



