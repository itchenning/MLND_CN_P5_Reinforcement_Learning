import random
import operator
import math

class Robot(object):

    def __init__(self, maze, alpha=0.5, gamma=0.9, epsilon0=0.5):

        self.maze = maze
        self.valid_actions = self.maze.valid_actions
        self.state = None
        self.action = None

        # Set Parameters of the Learning Robot
        self.alpha = alpha
        self.gamma = gamma

        self.epsilon0 = epsilon0
        self.epsilon = epsilon0
        self.t = 0

        self.Qtable = {}
        self.reset()

    def reset(self):
        """
        Reset the robot
        """
        self.state = self.sense_state()
        self.create_Qtable_line(self.state)

    def set_status(self, learning=False, testing=False):
        """
        Determine whether the robot is learning its q table, or
        exceuting the testing procedure.
        """
        self.learning = learning
        self.testing = testing

    def update_parameter(self):
        """
        Some of the paramters of the q learning robot can be altered,
        update these parameters when necessary.
        """
        if self.testing:
            # DOEN 1. No random choice when testing
            self.epsilon = 0
            pass
        else:
            # DONE 2. Update parameters when learning
            a = 0.05
            self.t += 1
            if self.epsilon <= 0:
                self.epsilon = 0
            else:
                self.epsilon = 0.5*math.cos(a * self.t)
            pass

        return self.epsilon

    def sense_state(self):
        """
        Get the current state of the robot. In this
        """

        # DONE 3. Return robot's current state
        return self.maze.sense_robot()

    def create_Qtable_line(self, state):
        """
        Create the qtable with the current state
        """
        # DONE 4. Create qtable with current state
        # Our qtable should be a two level dict,
        # Qtable[state] ={'u':xx, 'd':xx, ...}
        # If Qtable[state] already exits, then do
        # not change it.
        self.Qtable.setdefault(state, {a : 0.0 for a in self.valid_actions})
        pass

    def choose_action(self):
        """
        Return an action according to given rules
        """
        def is_random_exploration():

            # DONE 5. Return whether do random choice
            # hint: generate a random number, and compare
            # it with epsilon
            return random.random()<= self.epsilon

        if self.learning:
            if is_random_exploration():
                # DONE 6. Return random choose aciton
                return self.maze.valid_actions[random.randint(0,len(self.maze.valid_actions)-1)]
            else:
                # DONE 7. Return action with highest q value
                return max(self.Qtable[self.state], key=self.Qtable[self.state].get)
        elif self.testing:
            # DONE 7. choose action with highest q value
            return max(self.Qtable[self.state], key=self.Qtable[self.state].get)
        else:
            # DONE 6. Return random choose aciton
            return self.maze.valid_actions[random.randint(0,len(self.maze.valid_actions)-1)]

    def update_Qtable(self, r, action, next_state):
        """
        Update the qtable according to the given rule.
        """
        if self.learning:
            # DONE 8. When learning, update the q table according
            # to the given rules
            values = self.Qtable[self.state]
            next_values = self.Qtable[next_state]
            values[action] = (1 - self.alpha) * values[action] + self.alpha * (r + self.gamma * max(next_values.values()))

    def update(self):
        """
        Describle the procedure what to do when update the robot.
        Called every time in every epoch in training or testing.
        Return current action and reward.
        """
        self.state = self.sense_state() # Get the current state
        self.create_Qtable_line(self.state) # For the state, create q table line

        action = self.choose_action() # choose action for this state
        reward = self.maze.move_robot(action) # move robot for given action

        next_state = self.sense_state() # get next state
        self.create_Qtable_line(next_state) # create q table line for next state

        if self.learning and not self.testing:
            self.update_Qtable(reward, action, next_state) # update q table
            self.update_parameter() # update parameters

        return action, reward
