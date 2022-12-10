Created by Michael Perez
COP1047C (Intro to Python) Final Project

This is a game where the cat's objective is to collect all missing tails
while trying not to collide with the mouse. The game ends when the cat collects all tails
and a winning image appears. If the cat collides with the mouse, a losing image appears and 
the game ends.

How to play:
W - UP
A - LEFT
S - DOWN
D - RIGHT

#Note:

The original premise of the game was supposed to be a cat drawn out with no tail, with pieces
of its missing tail spread out across the map. The cat would then attempt to recollect the
pieces of its tail while trying not to collide with a cracked out mouse. Each piece collected
by the cat would update the cat's image and grow its tail, until all pieces were collected and
the cat fully recovered its tail.

But due to my chronic procrastination (it's a real thing) I did this last minute, and so I
ran into a a ton errors highlighted below:

- The grow function did not work, so I had to scratch the original idea. For the updated idea,
I should have instead just had the cat collect pieces of sashimi (it makes more sense)
- The radius at which collisions were being detected was far too large. The cat was picking
up tails while being nowhere near them, same goes for interactions with the mouse.
- The spawn points were totally messed up. I was able to make the cat, mouse, and tails
shuffle spawns randomly, but could not prevent them from spawning in the same place, which sometimes
led to the cat and mouse spawning directly on top of each other and instanteously ending the game.
