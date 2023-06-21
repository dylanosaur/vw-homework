import matplotlib
matplotlib.use('GTK3Agg')

import matplotlib.pyplot as plt
import numpy as np

# Generate some sample data
x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)

# Plot the data
plt.plot(x, y)
plt.xlabel('x')
plt.ylabel('sin(x)')
plt.title('Sine Wave')
plt.grid(True)

# Display the plot
plt.show()
