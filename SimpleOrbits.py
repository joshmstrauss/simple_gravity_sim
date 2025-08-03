# simple gravity simulation from scratch animated using matplotlib

import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
from matplotlib.widgets import Button
from matplotlib.collections import LineCollection

G = 6.673e-11 # Newton's gravitational constant

AU = 1.5e11
pi = math.pi
time_step = 600 * 60 # ten hours per frame

class Body:
    def __init__(self, name, mass, x, y, vx, vy, color):
        self.name = name
        self.mass = mass
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.trail = []

    def compute_gravitational_force(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.sqrt(dx**2 + dy**2) # compute the distance between self and other using the Pythagorean theorem

        if distance == 0:
            return (0, 0)

        force = G * self.mass * other.mass / distance**2  # Newton's Law of Gravitation
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
mercury = Body("Mercury", 0.33e24, 0, 0.39*AU, -47360, 0, 'gray')
venus = Body("Venus", 4.8673e24, 0.73 * AU * math.cos(1.25 * pi), 0.73 * AU * math.sin(1.25 * pi), 35020*math.cos(1.75*pi),35020*math.sin(1.75*pi), 'orange')
earth = Body("Earth", 5.972e24, AU, 0, 0, 2.978e4, 'blue')
mars = Body("Mars", 0.64e24, 0, -1.5*AU, 24080, 0, "red")
# moon = Body("Moon", 7.35e22, 1.5e11 + 3.84e8, 0, 0, 2.978e4 + 1022, 'gray') # added moon, but it's too small to see at scale

bodies = [sun, mercury, venus, earth, mars]

# set up plot
fig, ax = plt.subplots()
fig.patch.set_facecolor('black')    # sets figure background color
ax.set_facecolor('black')           # sets plot (axes) background color
ax.set_xlim(-4e11, 4e11)
ax.set_ylim(-4e11, 4e11)
scatter = ax.scatter([], [],)

# set up orbital trails (2D line objects)
trails = []
for b in bodies: 
    lc = LineCollection([], linewidths=1, colors=[b.color])
    ax.add_collection(lc)
    trails.append(lc)

def init():
    scatter.set_offsets([[0, 0]])
    for trail in trails:
        trail.set_segments([])
    return [scatter] + trails

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

        # store positions for trails
        body.trail.append((body.x, body.y))
        if len(body.trail) > 500:          # this sets trail length
            body.trail.pop(0)
        
        # update trail line
        xs_trail, ys_trail = zip(*body.trail)
        #trails[i].set_data(xs_trail, ys_trail)
        if len(body.trail) >= 2:
            segments = [body.trail[j:j+2] for j in range(len(body.trail)-1)]
            alphas = [(j + 1)/ len(segments) for j in range(len(segments))]
            colors = [(body.color, alpha) for alpha in alphas]
            trails[i].set_segments(segments)
            trails[i].set_colors(colors)
        else:
            trails[i].set_segments([])

    # draw updated positions
    xs = [b.x for b in bodies]
    ys = [b.y for b in bodies]
    cs = [b.color for b in bodies]
    scatter.set_offsets(list(zip(xs, ys)))
    scatter.set_facecolor(cs)
    scatter.set_sizes([100 if b.name == "Sun" else 10 for b in bodies])
    return [scatter] + trails

ani = animation.FuncAnimation(fig, update, init_func=init, frames=1000, interval=20, blit=True)
legend_patches = []
for body in bodies:
    patch = mpatches.Patch(color=body.color, label=body.name)
    legend_patches.append(patch)

ax.legend(handles=legend_patches, loc="upper right")
plt.title("Inner Solar System Simulation", color='white')
ax.tick_params(colors='white')
legend = ax.legend(handles=legend_patches, loc="upper right", facecolor='black')
for text in legend.get_texts():
    text.set_color("white")
plt.show()
        
