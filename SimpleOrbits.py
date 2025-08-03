# simple gravity simulation from scratch animated using matplotlib

import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches

G = 6.673e-11 # Newton's gravitational constant
time_step = 600 * 60 # one hour per frame

class Body:
    def __init__(self, name, mass, x, y, vx, vy, color):
        self.name = name
        self.mass = mass
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color

    def compute_gravitational_force(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.sqrt(dx**2 + dy**2) # compute the distance between self and other using the Pythagorean theorem

        if distance == 0:
            return (0, 0)

        force = G * self.mass * other.mass / distance**2
        angle = math.atan2(dy, dx)
        fx = math.cos(angle) * force    # compute force vector components using trig
        fy = math.sin(angle) * force
        return (fx, fy)

    def update(self, fx, fy, dt):
        ax = fx / self.mass
        ay = fy / self.mass
        self.vx += ax * dt
        self.vy += ay * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

# create bodies
sun = Body("Sun", 1.989e30, 0, 0, 0, 0, 'yellow')
earth = Body("Earth", 5.972e24, 1.5e11, 0, 0, 2.978e4, 'blue')
bodies = [sun, earth]

# set up plot
fig, ax = plt.subplots()
ax.set_xlim(-2e11, 2e11)
ax.set_ylim(-2e11, 2e11)
scatter = ax.scatter([], [],)

def init():
    return scatter,

def update(frame):
    forces = []

    # calculate forces on each body
    for body in bodies:
        total_fx, total_fy = 0, 0
        for other in bodies:
            if body == other:
                continue
            fx, fy = body.compute_gravitational_force(other)
            total_fx += fx
            total_fy += fy
        forces.append((total_fx, total_fy))
    
    # update each body with net force
    for i, body in enumerate(bodies):
        fx, fy = forces[i]
        body.update(fx, fy, time_step)

    # draw updated positions
    xs = [b.x for b in bodies]
    ys = [b.y for b in bodies]
    cs = [b.color for b in bodies]
    scatter.set_offsets(list(zip(xs, ys)))
    scatter.set_color(cs)
    scatter.set_sizes([100 if b.name == "Sun" else 10 for b in bodies])
    return scatter,

ani = animation.FuncAnimation(fig, update, init_func=init, frames=1000, interval=20, blit=True)
legend_patches = []
for body in bodies:
    patch = mpatches.Patch(color=body.color, label=body.name)
    legend_patches.append(patch)

ax.legend(handles=legend_patches, loc="upper right")

plt.title("Simple Gravity Simulation")
plt.show()
        
