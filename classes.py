class Room:

    all_rooms = []

    directions = ['north', 'east', 'south', 'west']

    def __init__(self, room_name, description):
        self.set_name(room_name)
        self.set_description(description)
        self.connected_rooms = {}

        Room.all_rooms.append(self) # Keep track of all room objects in Room class
    
    def __str__(self):
        return self.get_name()

    # SETTERS
    def set_name(self, name):
        self.name = name
    
    def set_description(self, description):
        self.description = description

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

    # GETTERS
    def get_name(self):
        return self.name[:]

    def get_description(self):
        if not self.description == None:
            return self.description
        else:
            return f'{self.get_name()} has no description'
        
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




    
    



