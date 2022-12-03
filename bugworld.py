import time
from random import choice, randint, random
from heapq import heappop, heappush
import turtle

class Bug:
    def __init__(self):
        self.hunger = 10
        self.life = 10
        self.position = (randint(0, 99), randint(0, 99))

    def move(self, disaster):
        # Use path finding to move to the nearest food
        x, y = self.position
        distances = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        heap = [(0, self.position)]
        visited = set()

        while heap:
            dist, pos = heappop(heap)
            if pos in visited:
                continue
            visited.add(pos)
            if food_grid[pos[0]][pos[1]] > 0:
                # Found food, move to this position
                self.position = pos
                return

            # Modify the movement based on the type of disaster
            if disaster == "flood":
                # Avoid moving in the direction of the flood
                if pos[0] < x:
                    distances.remove((-1, 0))
                elif pos[0] > x:
                    distances.remove((1, 0))
                if pos[1] < y:
                    distances.remove((0, -1))
                elif pos[1] > y:
                    distances.remove((0, 1))
            elif disaster == "fire":
                # Avoid moving in the direction of the fire
                if pos[0] > x:
                    distances.remove((1, 0))
                elif pos[0] < x:
                    distances.remove((-1, 0))
                if pos[1] > y:
                    distances.remove((0, 1))
                elif pos[1] < y:
                    distances.remove((0, -1))

            for dx, dy in distances:
                new_pos = (pos[0] + dx, pos[1] + dy)
                if 0 <= new_pos[0] < 100 and 0 <= new_pos[1] < 100:
                    heappush(heap, (dist + 1, new_pos))

    def find_food(self, food_grid):
        # Decrease the bug's hunger and life levels if it finds food
        x, y = self.position
        if food_grid[x][y] > 0:
            if eaten_grid[x][y] > 0:
                # The food has already been eaten, move to a different location
                self.move(disaster_grid[self.position[0]][self.position[1]])
            else:
                # The food hasn't been eaten, decrease the bug's hunger and life levels
                self.hunger -= 1
                self.life += 1
                food_grid[x][y] -= 1
                eaten_grid[x][y] += 1

    def reproduce(self):
        # Check if the bug's life level is high enough to reproduce
        if self.life >= 20:
            # Create a new bug at the current position
            new_bug = Bug()
            new_bug.position = self.position
            bugs.append(new_bug)

            # Generate a random color
            r = random()
            g = random()
            b = random()

            # Create a new turtle for the new bug
            new_turtle = turtle.Turtle()
            new_turtle.color(r, g, b)
            new_turtle.shape("turtle")
            bug_turtles.append(new_turtle)

            # Hide the new turtle
            new_turtle.hideturtle()

            # Update the position of the new turtle on the screen
            new_turtle.penup()
            new_turtle.goto(new_bug.position[0] * 10 - 500, new_bug.position[1] * 10 - 500)
            new_turtle.pendown()

            # Show the new turtle
            new_turtle.showturtle()

            # Decrease the bug's life level after reproducing
            self.life -= 10


def spawn_food(food_grid, season, prev_season):
    # Only spawn food if the current season is different from the previous season
    if season != prev_season:
        # Spawn food on a 100x100 grid
        for i in range(100):
            for j in range(100):
                # Only spawn food in certain seasons
                if season in ["spring", "summer"] and random() < 0.02:
                    food_grid[i][j] += 1
        # Set the color of the food_turtle object based on the season
        if season == "spring":
            food_turtle.color("green")
        elif season == "summer":
            food_turtle.color("orange")
        elif season == "autumn":
            food_turtle.color("brown")
        else:
            food_turtle.color("blue")
        return True
    else:
        return False


def spawn_disasters(disaster_grid, prev_disaster_grid):
    # Spawn disasters with probability 0.001
    disasters_spawned = False
    for i in range(100):
        for j in range(100):
            if random() < 0.00005:
                # Randomly choose a disaster type
                disaster_type = choice(list(disaster_types.keys()))

                # Spawn the disaster in a 3x3 area around the chosen location
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        x = i + dx
                        y = j + dy
                        if 0 <= x < 100 and 0 <= y < 100 and disaster_grid[x][y] == "":
                            disaster_grid[x][y] = disaster_type
                            disasters_spawned = True

    return disasters_spawned

num_bugs = 5
bugs = [Bug() for _ in range(num_bugs)]
food_grid = [[0] * 100 for _ in range(100)]

# Dictionary of disaster types, where the keys are the disaster types and the values are the corresponding turtle colors
disaster_types = {
    "flood": "blue",
    "drought": "brown",
    "fire": "red",
    "hurricane": "darkgrey",
    "blizzard": "grey"
}


# Initialize the turtle screen
screen = turtle.Screen()
screen.title("Bug Simulation")

# Create turtle objects for the bugs
bug_turtles = [turtle.Turtle() for _ in range(num_bugs)]
colors = ["red", "blue", "green", "orange", "purple"]
for t, color in zip(bug_turtles, colors):
    t.color(color)
    t.shape("turtle")

# Create a turtle object for the food
food_turtle = turtle.Turtle()
food_turtle.color("pink")
food_turtle.shape("square")
food_turtle.hideturtle()

# Create turtle objects for the disasters
disaster_turtles = {disaster_type: turtle.Turtle() for disaster_type in disaster_types}
for disaster_type, t in disaster_turtles.items():
    t.color(disaster_types[disaster_type])
    t.shape("square")
    t.hideturtle()

# Add a counter variable to keep track of the number of iterations
counter = 0

# Initialize prev_food_grid with the initial food grid
prev_food_grid = [row.copy() for row in food_grid]

# Add a list to store the locations of the food stamps
food_stamp_locations = []

# Add a variable to store the eaten grid
eaten_grid = [[0] * 100 for _ in range(100)]

# Initialize the disaster grid with empty strings
disaster_grid = [[""] * 100 for _ in range(100)]

# Initialize prev_disaster_grid with the initial disaster grid
prev_disaster_grid = [row.copy() for row in disaster_grid]

season = None

# Main simulation loop
while any(bug.life > 0 for bug in bugs):
    # Spawn disasters and check if any were spawned in the current iteration
    disasters_spawned = spawn_disasters(disaster_grid, prev_disaster_grid)

    for bug, t in zip(bugs, bug_turtles):
        if bug.life > 0:
            print("I'm feeling hungry!")
            bug.move(disaster_grid[bug.position[0]][bug.position[1]])
            bug.find_food(food_grid)
            bug.reproduce()

            # Update the turtle's position on the screen without drawing a line
            t.penup()
            t.goto(bug.position[0] * 10 - 500, bug.position[1] * 10 - 500)
            t.pendown()
        else:
            print("I'm dead :(")
            t.hideturtle()

        # Decrease the bug's life if it didn't find food
        if bug.hunger == 10:
            bug.life -= 1

            if bug.life > 100:
                bug.life = 0

    # Clear the food stamps that are no longer needed
    food_turtle.speed(0)
    food_turtle.penup()
    for i, j, stamp_id in food_stamp_locations:
        if food_grid[i][j] == 0 and prev_food_grid[i][j] > 0:
            food_turtle.clearstamp(stamp_id)

    # Determine the current season
    prev_season = season

    if counter < 200:
        season = "spring"
    elif counter < 350:
        season = "summer"
    elif counter < 450:
        season = "autumn"
    else:
        season = "winter"
        counter = 0

    # Spawn food based on the current season
    spawned_food = spawn_food(food_grid, season, prev_season)

    # Draw the food if it was spawned in the current iteration
    if spawned_food:
        # Draw a square at the location of each food item without animation or delay
        food_turtle.speed(0)
        food_turtle.penup()
        for i in range(100):
            for j in range(100):
                if food_grid[i][j] > 0 and prev_food_grid[i][j] == 0:
                    food_turtle.goto(i * 10 - 500, j * 10 - 500)
                    # Stamp the food at the current location
                    stamp_id = food_turtle.stamp()
                    # Add the stamp location to the list
                    food_stamp_locations.append((i, j, stamp_id))

    # Update the previous food grid with the current food grid
    prev_food_grid = [row.copy() for row in food_grid]

    # Only draw disasters when they're spawned or when starting the simulation
    if disasters_spawned or counter == 0:
        # Draw a square at the location of each disaster without animation or delay
        for disaster_type, t in disaster_turtles.items():
            t.speed(0)
            t.penup()
            for i in range(100):
                for j in range(100):
                    if disaster_grid[i][j] == disaster_type:
                        t.goto(i * 10 - 500, j * 10 - 500)
                        t.stamp()
            t.speed(10)

        # Update prev_disaster_grid
        prev_disaster_grid = [row.copy() for row in disaster_grid]

    # Increment the counter
    counter += 10
    time.sleep(1)

print("All bugs are dead.")
