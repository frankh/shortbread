shortbread
==========

Solver for a word puzzle. The puzzle is to find a path from one word to another only changing 
1 letter at a time and always passing through real words.

For example, the path from short -> bread is:

short
shoot
shook
shock
chock
crock
croak
creak
break
bread


Usage
=====

    $ python shortbread.py short bread
    path is ['short', 'shoot', 'shook', 'shock', 'chock', 'crock', 'croak', 'creak', 'break', 'bread']
    $ python shortbread.py -h
    Usage: shortbread.py [options] short bread
    
    Options:
      -h, --help            show this help message and exit
      -l LETTERS, --letters=LETTERS
                            valid letters - default is abcdef...xyz
      -d                    use depth first search
      -p, --precache        precache adjacent words graph
      -b                    use breadth first search. This is the default
  
Implementation
==============

It works by searching from both the start and end word until a common word is found.
