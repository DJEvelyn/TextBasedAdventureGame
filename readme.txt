Game starts by running tbag.py

Can get contextual commands with 'HELP' command.

Commands list:

LOOK - See the room's description
PICKUP (item) - Add an item to your inventory
INSPECT (item) - See an item's description
USE (item) >> (obstacle) <or> USE (item) ON (obstacle) - Item use command
GIVE (item) >> (obstacle) <or> GIVE (item) TO (obstacle) - Alternate item use command 
TALK TO (person) - Talk to person command
CONFRONT (obstacle) >> (item) <or> CONFRONT (obstacle) WITH (item) - Alternate item use command


// Critical path:

Go North [GO NORTH], Go West [GO WEST], Talk to Stranger [TALK TO STRANGER] and receive gold,
Go East [GO EAST], Use gold on Chef [USE GOLD >> CHEF / USE GOLD ON CHEF], Go north [GO NORTH],
Pickup Book [PICKUP BOOK], Go South [GO SOUTH], Use book on Guard [USE BOOK >> GUARD / USE BOOK ON GUARD],
Go East [GO EAST], Use book on Librarian [USE BOOK >> Librarian / USE BOOK ON LIBRARIAN], Go East [GO EAST],
Pickup key [PICKUP KEY], Go West [GO WEST], Go West [GO WEST], Go South [GO SOUTH], 
Use Key [USE KEY >> DOOR / USE KEY ON DOOR], Go South [GO SOUTH]

[GO NORTH]
[GO WEST]
[TALK TO STRANGER]
[GO EAST]
[USE GOLD >> CHEF / USE GOLD ON CHEF]
[GO NORTH]
[PICKUP BOOK]
[GO SOUTH]
[USE BOOK >> GUARD / USE BOOK ON GUARD]
[GO EAST]
[USE BOOK >> Librarian / USE BOOK ON LIBRARIAN]
[GO EAST]
[PICKUP KEY]
[GO WEST]
[GO WEST]
[GO SOUTH]
[USE KEY >> DOOR / USE KEY ON DOOR]
[GO SOUTH]


Other notes:

>> Branches were used, but merged into the main branch seamlessly.