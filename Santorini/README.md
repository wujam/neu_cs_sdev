# Santorini Design

## Files
- Design: Folder to contain implementation designs for Santorini pieces
  - board.py: the interface of a board for Santorini
  - player.py: the interface of a player component
  - rulechecker.py: interface of a rulechecker to be used by administrators and players
  - strategy.py: the interface for the strategy object
- Admin: Folder for all administrator-specific code
  - nothing here yet
- Player: Folder for all player-specific code
  - nothing here yet
- Common: Folder for all code that both administrative components and player components need to access
  - board.py: board implementation
  - rulechecker.py: rulechecker implementation
  - test_board.py: python script with unit tests for the board
  - test_rulechecker.py: python script with unit tests for the rule checker
- Lib: Folder for all library-like code
  - nothing here yet

Folders that would otherwise be empty contain an empty temp file becaues git doesn't allow empty directories
