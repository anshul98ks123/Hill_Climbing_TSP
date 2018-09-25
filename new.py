# load libraries
import math
from random import shuffle
import matplotlib.pyplot as plt

# open file
f = open('input.txt', 'r')

# read input from file
n = int(f.readline())
xcord = [float(x) for x in f.readline().split(' ')][:n]
ycord = [float(x) for x in f.readline().split(' ')][:n]

# initialize graph
plt.show()
axes = plt.gca()
line, = axes.plot(xcord, ycord, 'ro-')

# generate start state
x = [i for i in range(n)]

# calculates distance between two cities
def dist(x1, y1, x2, y2):
  return (math.sqrt((x1-x2)**2 + (y1-y2)**2))

# calculates heuristic cost of a state
def heuristic(xcord, ycord, x):
  total = 0
  for i in range(n):
    total = total + dist(xcord[x[i]], ycord[x[i]], xcord[x[(i+1)%n]], ycord[x[(i+1)%n]])
  return (total)

# generates new xcord and ycord values according to the order in solution
def newplot(xcord, ycord, x):
  newxcord = []
  newycord = []
  for i in range(n+1):
    newxcord.append(xcord[x[i%n]])
    newycord.append(ycord[x[i%n]])
  return (newxcord, newycord)

# visualize a solution
def draw(finished, iteration):
  # get new ordered coordinates of cities
  newxcord, newycord = newplot(xcord, ycord, x)

  # update graph
  line.set_xdata(newxcord)
  line.set_ydata(newycord)

  # update title 
  title = "Final " if finished else "iteration no. %d \n" % iteration
  title = title + ("total distance = %.2f" % heuristic(xcord, ycord, x))
  plt.title(title, fontsize = 12)

  # maximize window size of graph
  figManager = plt.get_current_fig_manager()
  figManager.window.showMaximized()

  # draw updated graph
  plt.draw()
  plt.pause(1.1)

def main():
  # hill climb algo
  for t in range(20):
    # draw intermediate solution
    draw(False, t+1)

    # cost of current state
    total = heuristic(xcord, ycord, x)

    print("iteration = ", t+1)
    print("total distance = %.2f" % total)

    newtotal = total
    swapi, swapj = -1, -1
    
    # apply rules
    for i in range(n):
      for j in range(n):
        if i != j:
          # successor
          newx = x.copy()
          newx[i], newx[j] = newx[j], newx[i]
          neighbour = heuristic(xcord, ycord, newx)

          # if successor is better than current, mark it
          if neighbour < newtotal:
            newtotal = neighbour
            swapi = i
            swapj = j
    
    if newtotal < total:
      # select the best successor
      x[swapi], x[swapj] = x[swapj], x[swapi]
      print(swapi, swapj)
    else:
      # halt 
      print("finish")
      break

  # show the final solution
  draw(True, 0)
  plt.show()

main()