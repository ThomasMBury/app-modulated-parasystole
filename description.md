


### Information:

###### Model overview
This is an interactive visualisation for a simple model of modulated parasystole 
([Courtemanche et al. (1989)](https://journals.physiology.org/doi/abs/10.1152/ajpheart.1989.257.2.H693)).
The model consists of two coupled oscillators. One oscillator represents the sinus rhythm,
which is the natural pacemaker of the heart. The other represents an ectopic focus, with a period
typically longer than that of the sinus rhythm. The oscillators are coupled according to the
following rules:

1. An ectopic beat is only expressed if it falls outside of the refractory period. The refractory period is the length
of time (theta) following a sinus beat, during which the heart cannot undergo a contraction.
2. The sinus beat immediately following an ectopic beat is suppressed.
3. Expressed sinus beats alter the ectopic period according to the phase response curve (PRC). For each expressed sinus beat
within an ectopic interval, the ectopic period is iteratively updated. The 'Pure' PRC corresponds to pure parasystole - 
the case where sinus beats have no impact on the ectopic period ([Glass et al. (1989)](https://www.ncbi.nlm.nih.gov/pubmed/3766761)). The PRC functions A-E are of increasing coupling between the 
ectopic period and sinus beats, and their explicit forms can be found in ([Courtemanche et al. (1989)](https://journals.physiology.org/doi/abs/10.1152/ajpheart.1989.257.2.H693)).


###### Key:
* **PRC**: phase response curve
* **ts**: period of the sinus pacemaker
* **te**: period of the ectopic pacemaker
* **theta**: refractory period of the heart
* **T**: modulated period of ectopic pacemaker due to intervening sinus beat
* **phi**: phase of a sinus beat within the ectopic period
* **NN**: interval corresponding to two consecutive sinus beats
* **NV**: interval corresponding to a sinus beat immediately followed by an ectopic beat
* **VN**: interval corresponding to an ectopic beat immediately followed by a sinus beat
* **VV**: interval corresponding to two consecutive ectopic beats
* **NIB**: number of intervening sinus beats between two ectopic beats

###### Panels:
* **Top-left**: control panel where parameter values for the simulation can be modified
* **Top-right**: selected phase response curve in bold, with the other PRCs also plotted
* **Middle-center**: interval length between two consecutive beats over time. The colour of the points indicates the type of beat that occurs at either end of the interval, as shown in the legend.
* **Bottom-left**: histogram showing the relative occurence of NIB values
* **Bottom-center**: histogram showing the distribution of NV and VN interval lengths
* **Bottom-right**: histogram for the inter-ectopic time interval

The graphs allow for zooming and scrolling with the mouse.

###### Notable configurations of (PRC, ts, te, theta):
* **('pure', 1, 2.3, 0.4)**: Pure parasystole triplet of NIB values (1,4,6) as expected theoretically ([Glass et al. (1989)](https://www.ncbi.nlm.nih.gov/pubmed/3766761)). Note the inter-ectopic intervals are multiples of a fixed number, te, as expected for pure parasystole.
* **('A', 1, 2.3, 0.4)**: Modulated parasystole with weak coupling preserves the triplet in many cases.
* **('D', 1, 2.3, 0.4)**: Strong coupling that results in stable trigeminy.
* **('E', 1, 2.3, 0.4)**: Strong coupling can result in silence of the ectopic beat - the PRC yields a map whereby the ectopic beat only ever lands in the refractory period of the sinus beat.
* **('B', 1, 2.04-2.09, 0.1)**: Concealed bigeminy (only NIB of the form 2n-1)
* **('B', 1, 3.29-3.34, 0.1)**: Concealed trigeminy (only NIB of the form 3n-1)












