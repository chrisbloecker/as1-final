#!/usr/bin/env python3

class Colour():
    BLACK = 0
    RED   = 1

class RedBlackTree():
    def __init__(self):
        pass

    def isEmpty(self):
        pass

    def size(self):
        pass

    def insert(self, element, key = id):
        pass

    def depth(self):
        pass

    def popMin(self):
        pass


class Empty(RedBlackTree):
    def __init__(self, key = id):
        RedBlackTree.__init__(self)
        self.key    = key
        self.colour = Colour.BLACK

    def __repr__(self):
        return "<Empty>"

    def __insert__(self, element):
        return self.insert(element)

    def isEmpty(self):
        return True

    def size(self):
        return 0

    def insert(self, element):
        return Node( element = element
                   , colour  = Colour.RED
                   , key     = self.key
                   )

    def balanceLeft(self):
        return self

    def depth(self):
        return 0

    def popMin(self):
        raise Exception("Empty tree!")

class Node(RedBlackTree):
    def __init__(self, element, colour = Colour.BLACK, key = id, left = None, right = None):
        RedBlackTree.__init__(self)
        self.element = element
        self.colour  = colour
        self.key     = key
        self.left    = left  if left  else Empty(key)
        self.right   = right if right else Empty(key)

    def __repr__(self):
        return "(<Node:{}:{}> {} {})".format(self.colour, self.element, self.left, self.right)

    def __insert__(self, element):
        if self.key(element) <= self.key(self.element):
            t = Node( element = self.element
                    , key     = self.key
                    , left    = self.left.__insert__(element)
                    , right   = self.right
                    )
        else:
            t = Node( element = self.element
                    , key     = self.key
                    , left    = self.left
                    , right   = self.right.__insert__(element)
                    )

        if self.colour == Colour.BLACK:
            t = t.balance()
        else:
            t.colour = Colour.RED

        return t

    def isEmpty(self):
        return False

    def size(self):
        return 1 + self.left.size() + self.right.size()

    def insert(self, element):
        t        = self.__insert__(element)
        t.colour = Colour.BLACK
        return t

    def mkRed(self):
        if self.colour == Colour.RED:
            raise Exception("This node was already RED!")

        return Node( element = self.element
                   , colour  = Colour.RED
                   , key     = self.key
                   , left    = self.left
                   , right   = self.right
                   )

    def balance(self):
        if self.left.colour == Colour.RED and self.right.colour == Colour.RED:
            t = Node( element = self.element
                    , colour  = Colour.RED
                    , key     = self.key
                    , left    = Node( element = self.left.element
                                    , key     = self.key
                                    , left    = self.left.left
                                    , right   = self.left.right
                                    )
                    , right   = Node( element = self.right.element
                                    , key     = self.key
                                    , left    = self.right.left
                                    , right   = self.right.right
                                    )
                    )

        elif self.left.colour == Colour.RED and self.left.left.colour == Colour.RED:
            t = Node( element = self.left.element
                    , colour  = Colour.RED
                    , key     = self.key
                    , left    = Node( element = self.left.left.element
                                    , key     = self.key
                                    , left    = self.left.left.left
                                    , right   = self.left.left.right
                                    )
                    , right   = Node( element = self.element
                                    , key     = self.key
                                    , left    = self.left.right
                                    , right   = self.right
                                    )
                    )

        elif self.left.colour == Colour.RED and self.left.right.colour == Colour.RED:
            t = Node( element = self.left.right.element
                    , colour  = Colour.RED
                    , key     = self.key
                    , left    = Node( element = self.left.element
                                    , key     = self.key
                                    , left    = self.left.left
                                    , right   = self.left.right.left
                                    )
                    , right   = Node( element = self.element
                                    , key     = self.key
                                    , left    = self.left.right.right
                                    , right   = self.right
                                    )
                    )

        elif self.right.colour == Colour.RED and self.right.right.colour == Colour.RED:
            t = Node( element = self.right.element
                    , colour  = Colour.RED
                    , key     = self.key
                    , left    = Node( element = self.element
                                    , key     = self.key
                                    , left    = self.left
                                    , right   = self.right.left
                                    )
                    , right   = Node( element = self.right.right.element
                                    , key     = self.key
                                    , left    = self.right.right.left
                                    , right   = self.right.right.right
                                    )
                    )

        elif self.right.colour == Colour.RED and self.right.left.colour == Colour.RED:
            t = Node( element = self.right.left.element
                    , colour  = Colour.RED
                    , key     = self.key
                    , left    = Node( element = self.element
                                    , key     = self.key
                                    , left    = self.left
                                    , right   = self.right.left.left
                                    )
                    , right   = Node( element = self.right.element
                                    , key     = self.key
                                    , left    = self.right.left.right
                                    , right   = self.right.right
                                    )
                    )
        else:
            t = Node( element = self.element
                    , key     = self.key
                    , left    = self.left
                    , right   = self.right
                    )

        return t

    def balanceLeft(self):
        if self.left.colour == Colour.RED:
            t = Node( element = self.element
                    , colour  = Colour.RED
                    , key     = self.key
                    , left    = Node( element = self.left.element
                                    , key     = self.key
                                    , left    = self.left.left
                                    , right   = self.left.right
                                    )
                    , right   = self.right
                    )

        elif self.right.colour == Colour.BLACK and not self.right.isEmpty():
            t = Node( element = self.element
                    , key     = self.key
                    , left    = self.left
                    , right   = Node( element = self.right.element
                                    , colour  = Colour.RED
                                    , key     = self.key
                                    , left    = self.right.left
                                    , right   = self.right.right
                                    )
                    ).balance()

        elif self.right.colour == Colour.RED and self.right.left.colour == Colour.BLACK and not self.right.left.isEmpty():
            t = Node( element = self.right.left.element
                    , colour  = Colour.RED
                    , key     = self.key
                    , left    = Node( element = self.element
                                    , key     = self.key
                                    , left    = self.left
                                    , right   = self.right.left.left
                                    )
                    , right   = Node( element = self.right.element
                                    , key     = self.key
                                    , left    = self.right.left.right
                                    , right   = self.right.right.mkRed()
                                    ).balance()
                    )

        elif self.left.isEmpty() or self.right.isEmpty():
            return self

        else:
            return self
            raise Exception("Unexpected case in balanceLeft!")

        return t

    def depth(self):
        return 1 + min(self.left.depth(), self.right.depth())

    # returns the minimum element and the new tree with the minimum removed
    def popMin(self):
        if self.left.isEmpty():
            return (self.element, self.right)

        (m, l) = self.left.popMin()

        return ( m
               , Node( element = self.element
                     , colour  = self.colour
                     , key     = self.key
                     , left    = l
                     , right   = self.right
                     ).balanceLeft()
               )


if __name__ == '__main__':
    from random import randint, random

    l = [randint(0, 100) for _ in range(100)]
    t = Empty()

    for x in l:
        t = t.insert(x)

    while not t.isEmpty():
        print(t.left.depth(), t.right.depth())
        m, t = t.popMin()
