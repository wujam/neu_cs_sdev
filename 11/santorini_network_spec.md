After the server initializes its internals, it enters a phase
where it waits for players to join.

      P1                 Server                  P2                          P3
	  |                    |(initializing)        |                          |
	  |                    |                      |                          |
	  |--------join------->|                      |                          |
	  |                    |                      |                          |
	  |<-----keepalive-----|                      |                          |
	  |------stillalive--->|                      |                          |
	  |<-----keepalive-----|                      |                          |
	  |------stillalive--->|                      |                          |
	  |                    |                      |                          |
	  |                    |<--------join---------|                          |
	  |<-----keepalive-----|                      |                          |
	  |------stillalive--->|                      |                          |
	  |                    |------keepalive------>|                          |
	  |                    |<-----stillalive------|                          |
	  |                    |                      |                          |
	  |                    |                      |                          |
	  |                    |<--------------------------------join------------|
	  |                    |                      |                          |
	  |                    |                      |                          |
      <-----set_id---------|---------set_id ------>---------set_id----------->

Message Formats:
|---------------|--------------------------------|--------------------------------|
| message_name  | structure                      | description                    |
|---------------|--------------------------------|--------------------------------|
| join          | ["join", string]               | join message with player name  |
|---------------|--------------------------------|--------------------------------|
| keepalive     | ["keepalive"]                  |                                |
|---------------|--------------------------------|--------------------------------|
| stillalive    | ["stillalive"]                 |                                |
|---------------|--------------------------------|--------------------------------|
| set_id        | ["set_id", string]             | set_id with Uuid as a string   |
|---------------|--------------------------------|--------------------------------|

Games are played between two players immediately after enough players are filled.
Players are not sent keepalives at this point, if a player's game starts and
they're sent a start_of_game and asked for placement, they're dqed for taking
too long if they don't respond back. These continue until all games are played
      P1                 Server                  P2
	  |                    |                      |
	  |                    |                      |
	  |<---start_of_game---|-----start_of_game--->|
	  |                    |                      |
	  |                    |                      |
	  |<---get_placement---|                      |
	  |---give_placement-->|                      |
	  |                    |-----get_placement--->|
	  |                    |<---give_placement----|
	  |<---get_placement---|                      |
	  |---give_placement-->|                      |
	  |                    |-----get_placement--->|
	  |                    |<---give_placement----|
	  |                    |                      |
	  |                    |-----get_turn-------->|
	  |                    |<----give_turn--------|
	  |<----get_turn-------|                      |
	  |----give_turn------>|                      |
	  -------------many turns later----------------
	  |<---end_game--------|------end_game------->|]



Message Formats:
|---------------|--------------------------------|-------------------------------------|
| message_name  | structure                      | description                         |
|---------------|--------------------------------|-------------------------------------|
| start_of_game | ["start_of_game"]              |                                     |
|---------------|--------------------------------|-------------------------------------|
| get_placement | ["get_placement"]              |                                     |
|---------------|--------------------------------|-------------------------------------|
| give_placement| ["give_placement", Placement]  | A Placement is                      |
|               |                                | [int:posx, int:posy]                |
|---------------|--------------------------------|-------------------------------------|
| get_turn      | ["get_turn"]                   |                                     |
|---------------|--------------------------------|-------------------------------------|
| give_placement| ["give_placement", Turn]       | A Turn is                           |
|               |                                | [Placement, Direction]              |
|               |                                |                                     |
|               |                                | A Placement is                      |
|               |                                | [int:posx, int:posy]                |
|               |                                | A Direction is a                    |
|               |                                |[NorthSouth, EastWest]               |
|               |                                | A NorthSouth is one of              |
|               |                                |   "North", "South", "Put"           |
|               |                                | A EastWest is one of                |
|               |                                |   "East", "West", "Put"             |
|---------------|--------------------------------|-------------------------------------|
| end_of_game   | ["end_of_game"]                |                                     |
|---------------|--------------------------------|-------------------------------------|