from matplotlib import pyplot as plt
import numpy as np
from scipy.integrate import cumtrapz
from ast import literal_eval
from shapely.geometry import Polygon

show_plot = True
save_figs = True

calculer_corde_aile = lambda longueur : -longueur*(133/755) + 0.606

calculer_contrainte_normale = lambda M, I, C, :-(M*C)/(I)

calculer_contrainte_cisaillement = lambda V, Q, I, t : (V*Q)/(I*t)
#x sur le long de l'aile en m
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
#chargement sur l'aile en n/m
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

corde = calculer_corde_aile(x)

coords_aile = '''1.00000000  0.00000000
0.99667566  0.00127091
0.98731466  0.00508030
0.97294285  0.01102133
0.95394941  0.01828860
0.93028455  0.02649819
0.90217220  0.03564269
0.87010598  0.04559033
0.83458560  0.05609031
0.79610663  0.06685087
0.75515297  0.07756051
0.71219794  0.08789714
0.66769773  0.09753021
0.62204386  0.10612640
0.57556669  0.11344647
0.52862389  0.11933627
0.48159244  0.12368504
0.43486602  0.12642440
0.38885365  0.12751147
0.34396060  0.12692343
0.30058729  0.12465754
0.25910372  0.12072122
0.21984312  0.11515990
0.18310506  0.10804821
0.14914254  0.09951468
0.11819963  0.08974616
0.09051427  0.07895233
0.06629112  0.06735503
0.04568918  0.05520889
0.02883347  0.04280482
0.01580501  0.03047906
0.00665698  0.01863245
0.00139717  0.00777183
0.00021738  0.00285253
0.00000128  0.00020630
0.00015578 -0.00218399
0.00047748 -0.00360344
0.00102029 -0.00482311
0.00188207 -0.00589101
0.00307710 -0.00690420
0.00536346 -0.00833777
0.00818256 -0.00966916
0.01396759 -0.01167125
0.02998040 -0.01489783
0.05146211 -0.01693984
0.07820223 -0.01780217
0.10998679 -0.01752983
0.14654017 -0.01622017
0.18753106 -0.01399145
0.23256226 -0.01100035
0.28117044 -0.00741551
0.33282653 -0.00342225
0.38695746  0.00080409
0.44295096  0.00506331
0.50015235  0.00915869
0.55787098  0.01286723
0.61535885  0.01597279
0.67182118  0.01826471
0.72640660  0.01957527
0.77822736  0.01980849
0.82641818  0.01896858
0.87014991  0.01711775
0.90865700  0.01440675
0.94123377  0.01098584
0.96708092  0.00711905
0.98551223  0.00347938
0.99640825  0.00091297
1.00000000  0.00000000'''

coords_aile = coords_aile.replace('  ', ', ')
coords_aile = coords_aile.replace(' -', ', -')
coords_aile = coords_aile.replace('\n', ', ')
coords_aile = literal_eval('[' + coords_aile + ']')

coords_aile_x = coords_aile[::2]
coords_aile_y = coords_aile[1::2]

aile = Polygon(list(zip(coords_aile_x, coords_aile_y)))


centroid_aile = aile.centroid



coords_aile_sup = [(x, y) if y > centroid_aile.y else (x, centroid_aile.y) for x, y in list(zip(coords_aile_x, coords_aile_y))]
#coords_aile_sup = [(x, y) for x, y in list(zip(coords_aile_x, coords_aile_y)) if y > centroid_aile.y]
coords_aile_sup_x = [i[0] for i in coords_aile_sup]
coords_aile_sup_y = [i[1] for i in coords_aile_sup]
aile_sup = Polygon(list(zip(coords_aile_sup_x, coords_aile_sup_y)))
centroid_aile_sup = aile_sup.centroid

coords_aile_inf = [(x, y) if y < centroid_aile.y else (x, centroid_aile.y) for x, y in list(zip(coords_aile_x, coords_aile_y))]
#coords_aile_inf = [(x, y) for x, y in list(zip(coords_aile_x, coords_aile_y)) if y < centroid_aile.y]
coords_aile_inf_x = [i[0] for i in coords_aile_inf]
coords_aile_inf_y = [i[1] for i in coords_aile_inf]
aile_inf = Polygon(list(zip(coords_aile_inf_x, coords_aile_inf_y)))
centroid_aile_inf = aile_inf.centroid

yc_c = 0.046128
max_dist = max([(abs(y - yc_c) + 0.00035) for y in coords_aile_y])
max_dist = max_dist*corde



Q_inf = aile_inf.area*abs(centroid_aile_inf.y - centroid_aile.y)
Q_sup = aile_sup.area*abs(centroid_aile_sup.y - centroid_aile.y)


I_revetement = 3.5e-4*0.0051752*corde**3
I_coeur = 9.8490e-5*corde**4
Q_coeur_sup = (aile_sup.area)*(abs(centroid_aile_sup.y - centroid_aile.y))*corde**3
Q_coeur_inf = (aile_inf.area)*(abs(centroid_aile_inf.y - centroid_aile.y))*corde**3
maskt = np.isclose(np.full_like(coords_aile_y, centroid_aile.y), coords_aile_y, 0.10)


t = np.array(coords_aile_x)[maskt]
t = abs(t[0]-t[1])*corde


V = cumtrapz(w, x, initial=0)
M = cumtrapz(V, x, initial=0)

V = np.array(V)
M = np.array(M)


V = -V[-1] + V
M = M[-1] - M


contrainte_normale = calculer_contrainte_normale(M, I_revetement, max_dist)

contrainte_cisaillement = calculer_contrainte_cisaillement(V, Q_coeur_inf, I_coeur, t)

print(f"""
Force cisaillement max: {np.max(np.abs(V)):.5g} N.
Moment fléchissant max: {np.max(np.abs(M)):.5g} Nm.
Contrainte normale max: {np.max(np.abs(contrainte_normale)):.5g} Pa ({np.max(np.abs(contrainte_normale))/1e6:.5g} MPa).
Contrainte cisaillement max: {np.max(np.abs(contrainte_cisaillement)):.5g} Pa ({np.max(np.abs(contrainte_cisaillement))/1e3:.5g} kPa).
Centroïde aile/c: ({centroid_aile.x:.5g}, {centroid_aile.y:.5g}).
Aire aile/c²: {aile.area:.5g} m².
Aire section supérieure/c²: {aile_sup.area:.5g} m².
Aire section inférieure/c²: {aile_inf.area:.5g} m².
Q section supérieure/c³: {Q_sup:.5g}.
Q section inférieure/c³: {Q_inf:.5g}.
Largeur max au centroide/c: {np.max(t/corde):.5g} m.
Distance max centroïde/c: {(max_dist/corde)[0]:.5g} m.
Facteur de sécurité en flexion : {700000000/np.max(np.abs(contrainte_normale)):.2f}
Facteur de sécurité en cisaillement : {600000/np.max(np.abs(contrainte_cisaillement)):.2f}
Facteur de sécurité en flexion avec un facteur de chargement de 3 : {(700000000/np.max(np.abs(contrainte_normale))/3):.2f}
Facteur de sécurité en cisaillement avec un facteur de chargement de 3 : {(600000/np.max(np.abs(contrainte_cisaillement)))/3:.2f}
""")

if show_plot == True:
    
    fig2 = plt.figure()
    fig2.canvas.manager.set_window_title("aile en 3D")
    fig2.suptitle("aile en 3D")
    ax = fig2.add_subplot(111, projection='3d')
    ax.axis('equal')
    coords_aile_x = np.array(coords_aile_x)
    coords_aile_y = np.array(coords_aile_y)

    for ci, z in zip(corde, x):
    
        x_scaled = coords_aile_x * ci
        y_scaled = coords_aile_y * ci
        
        ax.plot(x_scaled, y_scaled, z, zdir='y')



    fig4, axs4 = plt.subplots(1)
    fig4.canvas.manager.set_window_title("centroides des différentes parties de l'aile")
    fig4.suptitle("centroides des différentes parties de l'aile")
    axs4.axis('equal')

    axs4.plot(centroid_aile_inf.x, centroid_aile_inf.y, 'ro')
    axs4.plot(centroid_aile.x, centroid_aile.y, 'bo')
    axs4.plot(coords_aile_inf_x, coords_aile_inf_y, color='red')
    axs4.plot(coords_aile_sup_x, coords_aile_sup_y, color='green')
    axs4.plot(centroid_aile_sup.x, centroid_aile_sup.y,'go')
    axs4.axhline(centroid_aile.y, color='black', linewidth=1.5)



    fig1, axs1 = plt.subplots(1, 2, constrained_layout=False, figsize=(10,5))
    fig1.canvas.manager.set_window_title("diagrames de réactions de l'aile - V et M")
    fig1.suptitle("diagrames de réactions de l'aile - V et M")
    # V Plot
    axs1[0].plot(x, V)
    axs1[0].set_title('V')
    axs1[0].set_ylabel('N')
    axs1[0].set_xlabel('x (m)')
    axs1[0].axhline(0, color='black', linewidth=0.8)
    axs1[0].axvline(0, color='black', linewidth=0.8)
    axs1[0].grid(True)

    # M Plot
    axs1[1].plot(x, M)
    axs1[1].set_title('M')
    axs1[1].set_ylabel('Nm')
    axs1[1].set_xlabel('x (m)')
    axs1[1].axhline(0, color='black', linewidth=0.8)
    axs1[1].axvline(0, color='black', linewidth=0.8)
    axs1[1].grid(True)

    
    fig2, axs2 = plt.subplots(1, 2, constrained_layout=True, figsize=(10,5))
    fig2.canvas.manager.set_window_title("diagrames de réactions de l'aile - Contraintes")
    fig2.suptitle("diagrames de réactions de l'aile - Contraintes")
    # Contrainte Cisaillement Plot
    axs2[0].plot(x, contrainte_cisaillement/1e3)
    axs2[0].set_title('contrainte cisaillement')
    axs2[0].set_ylabel('kpa')
    axs2[0].set_xlabel('x (m)')
    axs2[0].axhline(0, color='black', linewidth=0.8)
    axs2[0].axvline(0, color='black', linewidth=0.8)
    axs2[0].grid(True)

    # Contrainte Normale Plot
    axs2[1].plot(x, contrainte_normale/1e6)
    axs2[1].set_title('contrainte normale')
    axs2[1].set_ylabel('Mpa')
    axs2[1].set_xlabel('x (m)')
    axs2[1].axhline(0, color='black', linewidth=0.8)
    axs2[1].axvline(0, color='black', linewidth=0.8)
    axs2[1].grid(True)


  

    fig5, axs5 = plt.subplots(1)
    fig5.canvas.manager.set_window_title("chargement en fonction de la position sur l'aile")
    fig5.suptitle("chargement en fonction de la position sur l'aile")
    axs5.plot(x, w)
    axs5.axhline(0, color='black', linewidth=0.8)
    axs5.axvline(0, color='black', linewidth=0.8)
    axs5.set_xlabel("position sur l'aile en m")
    axs5.set_ylabel("chargement en N/m")
    axs5.grid(True)

    fig1.savefig('figures/V_et_M.png')
    fig2.savefig('figures/Contraintes.png')
    fig4.savefig('figures/profile.png')
    fig5.savefig('figures/chargement.png')

    plt.show()





