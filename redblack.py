#!/usr/bin/env python3

# A (limited, unconventional) red black tree implementation.
# The red black tree can store more complicated data types than in usual
# implementations. We take a function to calculate the "size" of an element
# and insert it into the tree. Because we do that, we can associate additional
# data with an element.
#
# Implemented functionality is insert, retrieving the minimum element, and
# balancing (though the balancing might be incorrect).

# the identity function
identity = lambda x: x

# Colours to label the nodes.
class Colour():
    BLACK = 0
    RED   = 1


# The interface for a red black tree.
class RedBlackTree():
    def __init__(self):
        pass

    def checkInvariant(self):
        pass

    def isEmpty(self):
        pass

    def isRed(self):
        return self.colour == Colour.RED

    def isBlack(self):
        return self.colour == Colour.BLACK

    def size(self):
        pass

    def insert(self, element, key = identity):
        pass

    def balance(self):
        pass

    def depth(self):
        pass

    def popMin(self):
        pass


# An empty red black tree.
# Takes a key function at creation time that is used to "measure" the elements
# for insertion later. Empty nodes are black.
class Empty(RedBlackTree):
    def __init__(self, key = identity):
        RedBlackTree.__init__(self)
        self.key    = key
        self.colour = Colour.BLACK

    def __repr__(self):
        return "<Empty>"

    def __insert__(self, element):
        return self.insert(element)

    def checkInvariant(self):
        return True

    def isEmpty(self):
        return True

    def size(self):
        return 0

    def insert(self, element):
        return Node( element = element
                   , colour  = Colour.RED
                   , key     = self.key
                   )

    def balance(self):
        return self

    def balanceLeft(self):
        return self

    def depth(self):
        return 0

    def popMin(self):
        raise Exception("Empty tree!")


# A red black tree that contains data and children.
class Node(RedBlackTree):
    def __init__(self, element, colour = Colour.BLACK, key = identity, left = None, right = None):
        RedBlackTree.__init__(self)
        self.element = element
        self.colour  = colour
        self.key     = key
        self.left    = left  if left  else Empty(key)
        self.right   = right if right else Empty(key)

    def __repr__(self):
        return "(<Node:{}:{}> {} {})".format(self.colour, self.element, self.left, self.right)

    # "internal" method to insert a new element into the tree.
    # Performs rotations to balance the tree if necessary.
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

        if self.isBlack():
            t = t.balance()
        else:
            t.colour = Colour.RED

        return t

    def checkInvariant(self):
        return self.isBlack() or (self.left.isBlack() and self.right.isBlack())

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
        if self.left.isRed() and self.right.isRed():
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

        elif self.left.isRed() and self.left.left.isRed():
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

        elif self.left.isRed() and self.left.right.isRed():
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

        elif self.right.isRed() and self.right.right.isRed():
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

        elif self.right.isRed() and self.right.left.isRed():
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
        if self.left.isRed():
            print("#1")
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

        elif self.right.isBlack() and not self.right.isEmpty():
            print("#2")
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

        elif self.right.isRed() and self.right.left.isBlack() and not self.right.left.isEmpty():
            print("#3")
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

        elif self.isBlack() and not self.left.isEmpty() and self.left.isBlack() and self.left.right.isRed():
            print("#5")
            t = Node( element = self.left.right.element
                    , colour  = Colour.RED
                    , key     = self.key
                    , left    = Node( element = self.left.element
                                    , key     = self.key
                                    , left    = self.left.left
                                    , right   = self.left.right.left
                                    )
                    , right   = Node( element = self.left.right.element
                                    , key     = self.key
                                    , left    = self.left.right.right
                                    , right   = self.right
                                    ).balance()
                    )

        elif (self.left.isEmpty() and self.right.isEmpty()) or (self.isBlack() and self.left.isBlack() and self.right.isRed()):
            t = self

        else:
            print(self)
            raise Exception("Unexpected case in balanceLeft!")

        if (not t.left.isEmpty() and t.key(t.element) < t.key(t.left.element)) or (not t.right.isEmpty() and t.key(t.element) > t.key(t.right.element)):
            print(t)
            raise Exception("The tree is not sorted!")

        return t

    def depth(self):
        return 1 + min(self.left.depth(), self.right.depth())

    # returns the minimum element and the new tree with the minimum removed
    # the minimum element is always in the leftmost leaf of the tree.
    def popMin(self):
        if self.left.isEmpty():
            return (self.element, self.right)

        (m, l) = self.left.popMin()

        t = Node( element = self.element
                , colour  = self.colour
                , key     = self.key
                , left    = l
                , right   = self.right
                ).balance()

        t.checkInvariant()

        return (m, t)

    def getMin(self):
        if self.left.isEmpty() and self.right.isEmpty():
            return self.key(self.element)

        if self.left.isEmpty():
            return min(self.key(self.element), self.right.getMin())

        if self.right.isEmpty():
            return min(self.key(self.element), self.left.getMin())

        return min([self.key(self.element), self.left.getMin(), self.right.getMin()])


if __name__ == '__main__':
    from random import randint, random

    l = [randint(0, 1000) for _ in range(1000)]
    t = Empty()

    for x in l:
        t = t.insert(x)

    t.checkInvariant()

    while not t.isEmpty():
        shouldBeMin = t.getMin()
        m, t = t.popMin()

        if m != shouldBeMin:
            raise Exception("Wrong minimum, should be {} but is {}!".format(shouldBeMin, m))
