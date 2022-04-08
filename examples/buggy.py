from hpp.corbaserver import ProblemSolver
from hpp.environments import Buggy
from hpp.gepetto import PathPlayer  # noqa: F401
from hpp.gepetto import ViewerFactory

robot = Buggy("buggy")
robot.setJointBounds("root_joint", [-5, 16, -4.5, 4.5, -1.01, 1.01, -1.01, 1.01])

ps = ProblemSolver(robot)

gui = ViewerFactory(ps)

gui.loadObstacleModel("hpp_environments", "scene", "scene")

q_init = robot.getCurrentConfig()
q_goal = q_init[::]
q_init[0:2] = [-3.7, -4]
gui(q_init)

q_goal[0:2] = [15, 2]
gui(q_goal)

ps.setInitialConfig(q_init)
ps.addGoalConfig(q_goal)
ps.selectSteeringMethod("ReedsShepp")
ps.selectPathPlanner("DiffusingPlanner")
ps.addPathOptimizer("RandomShortcut")

t = ps.solve()
print("solving time", t)
