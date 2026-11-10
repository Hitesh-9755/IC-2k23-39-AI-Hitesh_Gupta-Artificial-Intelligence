"""
Vacuum Cleaner Problem
======================
A vacuum cleaner agent works in a grid world where each cell is either
clean or dirty.  The goal is to clean all dirty cells.

Two agent strategies are compared:
    1. Random agent      - picks a random legal action each step.
    2. Intelligent agent - moves toward the nearest dirty cell and
                           cleans when standing on a dirty cell.

Performance is measured by the number of steps taken.
"""

import random


class World:
    """Grid world with clean/dirty cells."""

    def __init__(self, width, height, dirty_cells):
        self.width = width
        self.height = height
        self.dirty_cells = list(dirty_cells)

    def is_dirty(self, pos):
        return pos in self.dirty_cells

    def clean(self, pos):
        if pos in self.dirty_cells:
            self.dirty_cells.remove(pos)

    def all_clean(self):
        return len(self.dirty_cells) == 0


class RandomVacuumAgent:
    """Agent that chooses a random legal action each step."""

    def __init__(self, world, start):
        self.world = world
        self.position = start
        self.steps = 0

    def _legal_actions(self):
        x, y = self.position
        actions = []
        if y + 1 < self.world.height:
            actions.append("UP")
        if y - 1 >= 0:
            actions.append("DOWN")
        if x + 1 < self.world.width:
            actions.append("RIGHT")
        if x - 1 >= 0:
            actions.append("LEFT")
        if self.world.is_dirty(self.position):
            actions.append("CLEAN")
        return actions

    def act(self):
        action = random.choice(self._legal_actions())
        x, y = self.position
        if action == "UP":
            self.position = (x, y + 1)
        elif action == "DOWN":
            self.position = (x, y - 1)
        elif action == "RIGHT":
            self.position = (x + 1, y)
        elif action == "LEFT":
            self.position = (x - 1, y)
        elif action == "CLEAN":
            self.world.clean(self.position)
        self.steps += 1

    def run(self, max_steps=1000):
        while not self.world.all_clean() and self.steps < max_steps:
            self.act()
        return self.steps


class IntelligentVacuumAgent:
    """Agent that greedily moves toward the nearest dirty cell."""

    def __init__(self, world, start):
        self.world = world
        self.position = start
        self.steps = 0

    @staticmethod
    def _manhattan(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def act(self):
        if self.world.is_dirty(self.position):
            self.world.clean(self.position)
            self.steps += 1
            return

        nearest = min(self.world.dirty_cells,
                      key=lambda d: self._manhattan(self.position, d))
        x, y = self.position
        dx = nearest[0] - x
        dy = nearest[1] - y

        if abs(dx) >= abs(dy) and dx != 0:
            new_pos = (x + (1 if dx > 0 else -1), y)
        elif dy != 0:
            new_pos = (x, y + (1 if dy > 0 else -1))
        else:
            new_pos = self.position

        nx, ny = new_pos
        if 0 <= nx < self.world.width and 0 <= ny < self.world.height:
            self.position = new_pos
        self.steps += 1

    def run(self, max_steps=1000):
        while not self.world.all_clean() and self.steps < max_steps:
            self.act()
        return self.steps


def make_world():
    """Create a 4x4 world with scattered dirty cells."""
    dirty = [(0, 0), (1, 2), (3, 1), (2, 3), (3, 3)]
    return World(width=4, height=4, dirty_cells=dirty)


def main():
    print("Vacuum Cleaner Problem - 4x4 Grid\n")

    # Intelligent agent
    world = make_world()
    agent = IntelligentVacuumAgent(world, start=(0, 3))
    steps = agent.run()
    print("Intelligent agent : %d steps, all clean = %s"
          % (steps, world.all_clean()))

    # Random agent (average over 10 trials)
    random.seed(42)
    trials = []
    for _ in range(10):
        world = make_world()
        agent = RandomVacuumAgent(world, start=(0, 3))
        trials.append(agent.run(max_steps=2000))
    print("Random agent      : avg %.1f steps over %d trials (min=%d, max=%d)"
          % (sum(trials) / len(trials), len(trials), min(trials),
             max(trials)))


if __name__ == "__main__":
    main()
