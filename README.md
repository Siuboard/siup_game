Current state of project:
Refactoring all modules, to make project more readable, more efficient
 and ready to expanding.

TODO:

1a). Board have to store information what kind of objects(States of
Fields) are declared. Then Pawn while is looking for possible actions,
 cares only for declared types. To make project more expansible, types
  should be stored in external file. Then also board_xml_generator have
  to get possible types from said file.
 
1). Refact Pawns, and way of checking its usable (LISKOV principle)

2). Relationship between Blocks, Pawns and Fields. 
Blocks, and Pawns should be stored as State of Field.

3). Way of execute program (Structure - name of module and obj to change)

4). board_xml_generator

5). Player whole module (ord of this one can be changed)
