"""
Basic Animation Simulation using matplotlib
A lightweight alternative to demonstrate the concept without Manim
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle

# Create figure and axis
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.set_title('Basic Math Animation - Circle Movement', fontsize=14, fontweight='bold')

# Create circle
circle = Circle((0, 0), 0.5, color='blue', alpha=0.7)
ax.add_patch(circle)

# Create text
text = ax.text(0, -4, '', ha='center', fontsize=12)

# Animation function
def animate(frame):
    # Move circle in a circular path
    angle = frame * 0.1
    x = 3 * np.cos(angle)
    y = 3 * np.sin(angle)
    circle.center = (x, y)
    
    # Update text
    text.set_text(f'Frame: {frame}\nAngle: {angle:.2f} rad\nPosition: ({x:.2f}, {y:.2f})')
    
    return circle, text

# Create animation
anim = animation.FuncAnimation(fig, animate, frames=100, interval=50, blit=True)

# Save animation as GIF
print("Generating animation...")
anim.save('simulation_output.gif', writer='pillow', fps=20)
print("✅ Animation saved as 'simulation_output.gif'")

# Display the animation
plt.show()
