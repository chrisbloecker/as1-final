#!/usr/bin/env python3

# This module provides modelling of obstacles in a scene and path planning to
# avoid those obstacles. Currently, Obstacles can be boxes that are described
# by scaling and translating unit cubes.

import numpy as np

# A 3D point.
class Point():
  def __init__(self, x, y , z):
    self.x = x
    self.y = y
    self.z = z

  def __repr__(self):
    return "({:.2f}, {:.2f}, {:.2f})".format(self.x, self.y, self.z)

  def distanceTo(self, point):
    return np.linalg.norm([self.x - point.x, self.y - point.y, self.z - point.z])


# An abstract object.
class Object():
  def __init__(self):
    pass

  # Checks whether the given point lies within the object.
  def contains(self, point):
    return False


# Scales an object according to the given scaling factors in x-, y-, and z-direction.
class Scale(Object):
  def __init__(self, scaledObject, scaleX, scaleY, scaleZ):
    self.scaledObject = scaledObject
    self.scaleX       = scaleX
    self.scaleY       = scaleY
    self.scaleZ       = scaleZ

  # Transforms the given point into the coordinate frame of the object and
  # checks whether the point lies within the object.
  def contains(self, point):
    scaledPoint = Point( point.x / self.scaleX
                       , point.y / self.scaleY
                       , point.z / self.scaleZ
                       )

    return self.scaledObject.contains(scaledPoint)


# Translates an object according to the given translations in x-, y-, and z-direction.
class Translate(Object):
  def __init__(self, translatedObject, translateX, translateY, translateZ):
    self.translatedObject = translatedObject
    self.translateX       = translateX
    self.translateY       = translateY
    self.translateZ       = translateZ

  # Translates the given point into the coordinate frame of the object and
  # checks whether the point lies within the object.
  def contains(self, point):
    translatedPoint = Point( point.x - self.translateX
                           , point.y - self.translateY
                           , point.z - self.translateZ
                           )

    return self.translatedObject.contains(translatedPoint)


# A unit cube.
class Cube(Object):
  def __init(self):
    Object.__init__(self)

  # The unit cube contains those points which have coordinates between 0 and 1
  # in all dimenstions.
  def contains(self, point):
    return 0 <= point.x <= 1 \
       and 0 <= point.y <= 1 \
       and 0 <= point.z <= 1


# A scene is represented as a cuboid and contains a set of obstacles that should
# be avoided in path planning. When constructed, the scene is represented as a
# regular cartesian grid according to the given resolution. The space is sampled
# and occupied grid cells are marked.
#
class Scene():
  def __init__(self, dimX, dimY, dimZ, resolution, obstacles):
    self.resolution = resolution
    self.bounds     = Scale(Cube(), dimX, dimY, dimZ)

    # number of grid cells in each direction
    x = int(dimX / resolution)
    y = int(dimY / resolution)
    z = int(dimZ / resolution)

    # to store which cells are occupied
    self.space = np.zeros((x, y, z))

    # Build the scene according to the given resolution and sample the space to
    # represent it as a 3D array with boolean values where True means that the
    # respective spot is occupied by an obstacle
    for i in range(x):
      for j in range(y):
        for k in range(z):
          p = Point((i + 0.5) * resolution, (j + 0.5) * resolution, (k + 0.5) * resolution)
          self.space[i, j, k] = any([obstacle.contains(p) for obstacle in obstacles])

  # Get the middle of a given grid cell (gx, gy, gz).
  def getPoint(self, gx, gy, gz):
    return Point( (gx + 0.5) * self.resolution
                , (gy + 0.5) * self.resolution
                , (gz + 0.5) * self.resolution
                )

  # Get the coordinate in the grid of a point.
  def getCoordinate(self, point):
    return ( int(point.x  / self.resolution)
           , int(point.y  / self.resolution)
           , int(point.z  / self.resolution)
           )

  # Use A* to plan a path from start to target and avoids the obstacles in the scene.
  def planPath(self, start, target):
    # the start point must be within the scene
    if not self.bounds.contains(start):
      raise Exception("Start ({:.2f}, {:.2f}, {:.2f}) is out of bounds!".format(start.x, start.y, start.z))

    # the target point must be within the scene
    if not self.bounds.contains(target):
      raise Exception("Target ({:.2f}, {:.2f}, {:.2f}) is out of bounds!".format(target.x, target.y, target.z))

    # the grid cells corresponding to start and target
    startX,  startY,  startZ  = self.getCoordinate(start)
    targetX, targetY, targetZ = self.getCoordinate(target)

    # the start point must not lie within an obstacle
    if self.space[startX, startY, startZ]:
      raise Exception("Start {} point lies within an obstacle!".format(self.getPoint(startX, startY, startZ)))

    # the target point must not lie within an obstacle
    if self.space[targetX, targetY, targetZ]:
      raise Exception("Target {} point lies within an obstacle!".format(self.getPoint(targetX, targetY, targetZ)))

    explored   = set()
    unexplored = { (startX, startY, startZ) : start.distanceTo(target) }
    cameFrom   = {}

    # continue planning as long as we have unexplored grid cells left
    while len(unexplored) > 0:
      (currentX, currentY, currentZ), currentCost = min(unexplored.items(), key = lambda p: p[1])
      unexplored.pop((currentX, currentY, currentZ))
      explored.add((currentX, currentY, currentZ))

      if currentX == targetX and currentY == targetY and currentZ == targetZ:
        return self.reconstructPath(cameFrom, (currentX, currentY, currentZ), target)

      p = self.getPoint(currentX, currentY, currentZ)

      for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
          for dz in [-1, 0, 1]:
            x = currentX + dx
            y = currentY + dy
            z = currentZ + dz

            q = self.getPoint(x, y, z)

            if (x, y, z) not in explored and self.bounds.contains(q) and not self.space[x, y, z]:
              cost = currentCost + q.distanceTo(target)

              if (x, y, z) not in unexplored or cost < unexplored[(x, y, z)]:
                unexplored[(x, y, z)] = cost
                cameFrom[(x, y, z)]   = (currentX, currentY, currentZ)

    raise Exception("Cannot find a path to target!")

  def reconstructPath(self, cameFrom, endpoint, target):
    path = [ target
           , self.getPoint(endpoint[0], endpoint[1], endpoint[2])
           ]

    while endpoint in cameFrom:
      endpoint = cameFrom[endpoint]
      path.append(self.getPoint(endpoint[0], endpoint[1], endpoint[2]))
    return path[::-1]


if __name__ == '__main__':
    table1 = Translate(Scale(Cube(), 1.30, 0.65, 0.75), 1.35, 0.68, 0.00)
    table2 = Translate(Scale(Cube(), 1.30, 0.65, 0.75), 1.35, 2.68, 0.00)

    obstacle = Translate(Scale(Cube(), 1.60, 0.8, 2.20), 1.25, 1.70, 0.00)

    scene  = Scene(4.0, 4.0, 2.5, 0.1, [table1, table2, obstacle])
    start  = Point(2.0, 1.0, 0.9)
    target = Point(2.0, 3.0, 0.9)

    path = scene.planPath(start, target)

    print(path)

    pathLength = 0
    i = 1
    while i < len(path):
        pathLength += path[0].distanceTo(path[1])
        i += 1
    print(pathLength)
