Adrian Grzywaczewski 1204969
# Simple MMORPG Game: Looting Dungeons

## Link to the video and screenshots from the game:
[Demo and Screenshots of the game](https://drive.google.com/drive/folders/13lJTBlTZSOOzJkUfA4VZ7t51VL-jANBG?usp=sharing)

## Key facts about the game:

* Simple MMORPG Game.
* Based in Fantasy World.
* The game has been inspired by a very old game called [Tibia](https://www.tibia.com)
that I used to play when I was younger. This game is over 20 years old and still has thousands of active players.
* Graphics and sprites that have been used for this project come from this game.

## Working features of the game:

* Authentication
  * User can register an account ( player ).
  * User can log in as an existing player.
  * User can edit details of the account/player.

### Adventure
* System spawns 3 monsters for each player.
* Player can decide which monster to attack/kill
* Player can kill monsters.
* When a monster is being attacked:
  * Monster dynamically uses health points. A player can see "live" the dropping hp of the monster.
  * In a case when a user logs out and logs in back to the game he can see.
  * The damage dealt with the monster is being logged in the log area.
  
* When a player kills a monster then he:
  * Gets experience points.
  * Gets gold.
  * Loots items.
  * Information about the gained experience, loot, gold is being displayed to the user in the log area.
  * Items, gold, experience of a player are being updated dynamically.
  
* Each monster has:
  * A Unique number of health points.
  * A Unique number of experience points that it gives to a player.
  * Monsters drop specific items that are assigned to them.
  * The information about what monster drops what item can be only acquired from other players.
  

* Player can wear items he looted as an equipment.
* Player can see the equipment that he wears.
* Player can see a list of items that he looted and wear/equip any of them.
* Player can sell an item to other players.
* Player can compete with other players. Players are being ranked based on the number of experience points they collected.
* The higher level of a player the higher damage dealt with monsters.
* The weapon that is equipped increases the damage dealt by a player to monsters.

### Market

* Player can buy an item from another player from the market.
* All items available for sale are listed on the market list.
* When a player buys an item:
  * The owner of the item gets the money for the item. 
  ( If an item has been placed on the market for 10 gold then he will receive that amount)
  * The item disappears from the market so it is not available to other players.
  * Player who bought an item can see this item in his items list.
  * The acquired item can be equipped.

### Chat
* Players can use chat to talk with each other in real time.
* Players see the level of other players that they are talking to.
* Players can negotiate prices for the items that they want to buy from other players.
* Players can share the knowledge about what items are being dropped by each monster.


# Main technologies used:

### Backend:

* [Python](https://www.python.org/) - Programming language
* [Django](https://www.djangoproject.com/) - Web development framework
* [PostgreSQL](https://www.postgresql.org/) - Database

### Frontend:

* Javascript
* jQuery
* HTML
* CSS

### Other:

* [Pusher](https://pusher.com/) - Chat notifications
* Other libraries specified in requirements.txt file

### Future improvements

* Boss raids where a group of at least 5 players has to defeat a boss.
* Function that allows monster to attack user if they are attacked.
* Monsters should respectively to player's level. Stronger player should get strong monsters to fight with.
