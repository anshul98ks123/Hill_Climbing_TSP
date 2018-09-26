# load libraries
import math
import matplotlib.pyplot as plt

# open file
f = open('input.txt', 'r')

# read input from file
# number of cities and x and y coordinates
n = int(f.readline())
xcord = [float(x) for x in f.readline().split(' ')][:n]
ycord = [float(x) for x in f.readline().split(' ')][:n]

# initialize graph
plt.show()
axes = plt.gca()
line, = axes.plot(xcord, ycord, 'ro-')

# calculates euclidean distance between two cities
def dist(xcord, ycord, i, j):
  x1 = xcord[i]
  y1 = ycord[i]
  x2 = xcord[j]
  y2 = ycord[j]
  return (math.sqrt((x1-x2)**2 + (y1-y2)**2))

# generate start state and the ordered coordinates
x = [i for i in range(n)]
xcord = [xcord[x[i]] for i in range(n)]
ycord = [ycord[x[i]] for i in range(n)]

# calculate cosr of start state
initial_cost = sum([dist(xcord, ycord, i, (i+1)%n) for i in range(n)])

# calculates heuristic cost of a state
def heuristic(xcord, ycord, i, j, current_cost):
  total = current_cost

  # special case of 0 and n-1, we swap i and j
  if i == 0 and j == n-1:
    i, j = j, i

  if j!=(i+1)%n:
    # if i and j are not adjacent
    total -= dist(xcord, ycord, i, (i+1)%n)
    total -= dist(xcord, ycord, j, (j-1+n)%n)
    total += dist(xcord, ycord, j, (i+1)%n)
    total += dist(xcord, ycord, i, (j-1+n)%n)

  total -= dist(xcord, ycord, i, (i-1+n)%n)
  total -= dist(xcord, ycord, j, (j+1)%n)
  total += dist(xcord, ycord, i, (j+1)%n)
  total += dist(xcord, ycord, j, (i-1+n)%n)
  return (total)

# visualize a solution
def draw(finished, iteration, cost):
  # add cord of first city to end 
  # to draw an edge from last to first city
  newxcord = xcord.copy() + [xcord[0]]
  newycord = ycord.copy() + [ycord[0]]

  # update graph
  line.set_xdata(newxcord)
  line.set_ydata(newycord)

  # update title of the graph 
  title = "Final " if finished else "iteration no. %d \n" % iteration
  title = title + ("total distance = %.2f \n" % cost)
  plt.title(title, fontsize = 15)

  # maximize window size of graph
  figManager = plt.get_current_fig_manager()
  figManager.window.showMaximized()

  # draw updated graph
  plt.draw()
  plt.pause(0.1)

def main(xcord, ycord, initial_cost, x):
  current_cost = initial_cost

  # hill climb algo limited to 200 iterations
  for t in range(200):
    # draw intermediate solution
    draw(False, t+1, current_cost)

    # cost of current state
    print("iteration = ", t+1)
    print("total distance = %.2f" % current_cost)

    newtotal = current_cost
    swapi, swapj = -1, -1
    
    # apply rules
    for i in range(n):
      for j in range(n):
        if i != j and i < j:
          # get heuristic cost of successor
          neighbour = heuristic(xcord, ycord, i, j, current_cost)

          # if successor is better than current, mark it as best successor
          if neighbour < newtotal:
            newtotal = neighbour
            swapi = i
            swapj = j

    if newtotal < current_cost:
      # select the best successor and apply the rule
      x[swapi], x[swapj] = x[swapj], x[swapi]
      xcord[swapi], xcord[swapj] = xcord[swapj], xcord[swapi]
      ycord[swapi], ycord[swapj] = ycord[swapj], ycord[swapi]
      current_cost = newtotal
      print("swapped ", swapi, swapj)
    else:
      # halt 
      print("finish")
      break

  # show final stats
  print("Final order = ", x)
  print("Initial cost = ", initial_cost)
  print("Final cost = ", current_cost)
 
  # show the final solution
  draw(True, 0, current_cost)
  plt.show()

main(xcord, ycord, initial_cost, x)