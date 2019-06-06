# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 13:53:29 2019

@author: patri
"""

import numpy as np
import matplotlib.pyplot as plt
from Class_II import *

###This programme gives a class II weight estimation for a cargo aircraft based on the Raymer empirical data

W_wing = 0.0051*(W_dg*N_z)**0.557*S_w**0.649*A**0.5*(t_c_root)**-0.4*(1+taper_ratio)**0.1*np.cos(np.deg2rad(sweep))**-1.0*S_csw**0.1

W_ht = 0.0379*K_uht*(1+F_w/B_h)**-0.25*W_dg**0.639*N_z**0.1*S_ht**0.75*L_t**-1.0*K_y**0.704*np.cos(np.deg2rad(sweep_ht))**-1.0*A_h**0.166*(1+S_e/S_ht)**0.1

W_vt = 0.0026*(1 + H_t/H_v)**0.225*W_dg**0.556*N_z**0.536*L_t**-0.5*S_vt**0.5*K_z**0.875*np.cos(np.deg2rad(sweep_vt))**-1*A_v**0.35*(t_c_root_vt)**-0.5

W_fus = 0.328*K_door*K_Lg*(W_dg*N_z)**0.5*L**0.25*S_f**0.302*(1+K_ws)**0.04*(L/D)**0.1

W_main_gear = 0.0106*K_mp*W_l**0.888*N_l**0.25*L_m**0.4*N_mw**0.321*N_mss**-0.5*V_stall**0.1

W_nose_gear = 0.032*K_np*W_l**0.646*N_l**0.2*L_n**0.5*N_nw**0.45

W_nacelle_group = 0.6724*K_ng*N_Lt**0.1*N_w**0.294*N_z**0.119*W_ec**0.611*N_en**0.984*S_n**0.224

W_engine_controls = 5.0*N_en + 0.80*L_ec

W_fuel_system = 2.405 * V_t**0.606*(1+V_i/V_t)**-1.0*(1+V_p/V_t)*N_t**0.5*S_cs**0.2*(I_y*10**-6)**0.07

#W_APU_installed=2.2*W_APU_uninstalled

W_instruments = 4.509 * K_r*K_tp*N_c**0.541*N_en*(L_f + B_w)**0.5

W_hydraulics = 0.2673*N_f*(L_f + B_w)**0.937

W_electrical = 7.291*R_kva**0.782*L_a**0.346*N_gen**0.1

W_avionics = 1.73*W_uav**0.983

W_anti_ice = 0.002*W_dg

#W_furnishings = 0.0577*N_c**0.1*W_c**0.393*S_f**0.75  

