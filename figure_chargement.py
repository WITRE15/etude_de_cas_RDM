import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

x : list = [0.0,
 0.05373,
 0.16462,
 0.27075,
 0.37686,
 0.48139,
 0.58116,
 0.67934,
 0.77119,
 0.86503,
 0.95031,
 1.03409,
 1.10989,
 1.1782,
 1.24301,
 1.30034,
 1.35267,
 1.3985,
 1.43635,
 1.46621,
 1.48857,
 1.50244,
 1.50782,
 1.51]

w : list = [64.227,
 63.854,
 63.021,
 61.875,
 60.208,
 58.333,
 56.354,
 54.063,
 51.875,
 49.528,
 47.034,
 44.344,
 41.719,
 38.93,
 36.141,
 33.188,
 30.268,
 26.725,
 23.181,
 19.342,
 15.11,
 10.418,
 5.824,
 0.0]

x = np.array(x)
w = np.array(w)

plt.axis(False)
plt.plot(x, w, color='b')
plt.plot([0, x[-1]], [0, 0], color='black', linewidth=2 )
plt.plot([0, x[-1]], [-20,-20], color='black', linewidth=2 )
plt.plot([0, 0], [10,-30], color='black', linewidth=2 )
plt.plot([x[-1], x[-1]], [0,-20], color='black', linewidth=2 )



start_points_x = x[0:-3]
start_points_y = w[0:-3]       
dx = np.zeros_like(start_points_x)       
dy = -start_points_y      

plt.fill_between(([0,x[-1]]), 0, -20)
plt.quiver(-0.05, -20 , 0, 20, color='r', angles='xy', scale_units='xy', scale=1, label='force de réaction')
plt.quiver(start_points_x, start_points_y, dx, dy, color='b', angles='xy', scale_units='xy', scale=1, label='chargement')
curved_arrow = patches.FancyArrowPatch((-0.095, 0), (-0.095, -20),
                                       connectionstyle="arc3,rad=-0.4",
                                       arrowstyle="Simple,tail_width=1.5,head_width=6,head_length=10",
                                       color="green",
                                       label='moment de réaction')
plt.gca().add_patch(curved_arrow)
plt.gca().invert_yaxis()
plt.legend(loc='lower right')
plt.savefig('figures/DCL.png')
plt.show()