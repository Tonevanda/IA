# Focus 

## Dependencies

- pygame
- numpy

To install these dependencies, simply run the `install.sh` like so:

```sh
sh src/install.sh
```

## How to play

To run the game, run the following command on your terminal:

```sh
python3 src/main.py
```

The goal of this game is to make it so that your opponent cannot make a move.
See **[rules](#rules)** for more information

This game is played entirely using your **mouse**, except for certain actions like **starting a game** or **quitting**, where you press a certain key on your **keyboard**.

- To move a *piece/stack*, simply click on it with your **mouse**, and select the cell where you wish to move the *piece/stack* to.
- To play a *piece* from your *personal* stack, as in your own captured pieces that are not on the board, click the *piece* symbol at the top-right/top-left of the screen, depending on what color player you are, and select the cell where you wish to place that *piece*.
- Additionally, if you want a little help with your move, you can click the lightbulb symbol on the screen and get a **hint** for a possible good move to play in that position.

### Rules

- [x] Two to four players move stacks of one to five pieces (depends on the size of the board) around a checkerboard with the corners cut out.
- [x] Stacks may move as many spaces as there are pieces in the stack. 
- [x] Players may only move a stack if the topmost piece in the stack is one of their pieces. 
- [x] When a stack lands on another stack, the two stacks merge; if the new stack contains more than five pieces, then pieces are removed from the bottom to bring it down to five. 
- [x] If a player's own piece is removed, they are kept and may be placed on the board later in lieu of moving a stack. If an opponent's piece is removed, it is captured. The last player who is able to move a stack wins.

## Developed by 🧑🏻‍💻

- **Tiago Cruz** - [@Tiago27Cruz](https://www.github.com/Tiago27Cruz)
- **João Lourenço** - [@Tonevanda](https://www.github.com/Tonevanda)
- **Tomás Xavier** - [@dratomitoma](https://www.github.com/dratomitoma)