# Heat Equation for 1-Dimensional Rod
In this animation (made using the [`matnimation`](https://github.com/timdewild/matnimation/tree/main) module), we model the cooling of a 1-dimensional metal rod, subject to different boundary conditions (BCs). 

## Solving the Heat Equation
We will solve the heat equation for a 1-dimensional metal rod of unit length. Of course, 1-dimensional rods do not exist, but this is a very good approximation for rods whose thickness $d$ is much smaller then their length $L$. The location along the rod is indicated by the the coordinate $x$. The temperature along the rod at a given moment in time $t$ is denoted by $u(x,t)$. 

The question we wish to answer is the following: given the temperature distribution along the rod at $t=0$, what will be the temperature distribution at all subsequent times $t>0$? 

The time-evolution of the temperature $u$ is given by a partial differential equation (PDE) called the heat equation:

$$u_t = D u_{xx},$$

where $D$ is the thermal diffusivity and subscripts denote partial derivatives with respect to the subscripted variable. We will work in units such that the bar has unit length and hence $x\in [0,1]$.  To solve this PDE, we need two extra ingredients: initial and boundary conditions.

### Initial Conditions
Initial conditions describe the state of the system at the initial time. In our case, this is the temperature distribution along the rod at time $t=0$, which we denote by $f(x)$. That is:

$$u(x,0)\equiv f(x), \quad x\in[0,1].$$

### Boundary Conditions
We have to specify the behavior at the two ends, or boundaries, of the rod:

$$x_0 = \\{0,1\\}.$$ 

Different boundary conditions (BCs) yield very different solutions and also reflect different assumptions about the physical characteristics of the system. 

- **Uniform Dirichlet BCs:** In this case we assume that the temperature is fixed to be the same value $T_\infty$ on both ends of the rod at all times:
$$u(x_0,t) = T_\infty.$$ These BCs are applicable in case the rod is in connection with an infinite thermal bath kept at temperature $T_\infty$. Heat will be exchanged between the rod and the bath such that the rod will get into thermal equilibrium with the bath at $T_\infty$. 

- **Uniform Neumann BCs:** In this case we assume that the rod is perfectly insulated and no heat can flow in or out of the rod. Mathematically, this amounts to the spatial derivative being zero: $$u_x(x_0,t) = 0.$$ With those BCs, the heat in rod will distribute uniformly over the rod such that the temperature becomes uniform everywhere along the rod, irrespective of what the initial temperature distribution was. 

Given the initial and boundary conditions, the heat equation can be solved using the Fourier series. (Actually, Joseph Fourier discovered what we now know as Fouries series when solving the heat equation back in the 19-th century). 

- For **uniform Dirichlet BCs**, the solution is:
$$u(x,t) = \sum_{n=1}^\infty b_n e^{-\lambda_n^2 t}\cos(\mu_n x),$$ where we defined $\lambda_n \equiv cn\pi$, $\mu_n \equiv n\pi$ and $c\equiv \sqrt{D}$. The coefficients $b_n$ are the cosine Fourier coefficients: $$b_n = \int_0^1 dx\\; f(x)\sin(n\pi x).$$

- For **uniform Neumann BCs**, the solution is:
$$u(x,t) = a_0+\sum_{n=1}^\infty b_n e^{-\lambda_n^2 t}\cos(\mu_n x),$$ where the coefficients $a_n$ are the sine Fourier coefficients: $$a_0 = \int_0^1 dx\\; f(x),\quad a_n = 2\int_0^1 dx\\; f(x)\cos(\mu_n x).$$ Note that the coefficient $a_0$ is the (spatial) average of the initial temperature distribution $f(x)$:
$$a_0 = \bar{f}.$$ As $t\to\infty$, the solution asymptotes to $u(x,t)\to a_0$. This is to be expected, since the bar is insulated and the thermal energy distributes evenly over the bar so that the rod acquires a constant temperature everywhere. It is not suprising that this temperature is equal to the average of the initial temperature profile. 

> [!NOTE]
> In the animations, the evolution of the temperature profile over time is shown in the upper panel. 

## Heat Flux: Fourier's Law
In addition to the evolution of the temperature over time, it is also interesting to look at the heat flux in the rod. The flux tells us how heat flows through the rod over time. We define heat flux density $\vec{q}$ as the amount of thermal energy $dE$ flowing though an area element $d\vec{A}= dA\\;\hat{n}$ in time interval $dt$. This is given by:
$$\vec{q} = \frac{dE}{dA\\;dt}.$$
Energy flows from hot regions to cold regions, so as to get the whole system into thermal equilibrium. Therefore, we expect the heat flux $\vec{q}$ to be proportional to the negative gradient of the temperature:
$$\vec{q} = -k\vec{\nabla} u,$$
where the proportionality constant $k$ is the thermal conductivity. In our one-dimesional case, we have:
$$\vec{q}(x,t) = -k u_x(x,t)\hat{x}.$$

> [!NOTE]
> In the animations, the middle panel gives temperature distribution along the rod by means of a heatmap. Vectors representing the heat flux $\vec{q}$ are superimposed on this heatmap in white. 

## Atomic Lattice Vibrations
At the microscopic level, the metal rod consists of a lattice, with atoms at the nodes of the lattice. Classically, one may think of the atoms being connected to each other via small springs, so that energy from one can be transferred from one atom to a neighbouring atom. The atoms vibrate about their equilibrium position in the lattice. The higher the temperature, the faster the atoms oscillate/vibrate in the lattice. In case of a temperature gradient in the rod, the atoms in hotter regions transfer part of their kinetic energy to atoms in colder regions. The kinetic energy of the latter will increase, making them vibrate faster. The former will lose kinetic energy, and start vibrating slower. Once the temperature is evenly distributed along the rod, all atoms in lattice vibrate at the same pace.  

> [!NOTE]
> In the animations, the lower panels shows the atoms (blue dots) vibrating in the atomic lattice. Although it is sometimes difficult to tell at first glance (play the animations multiple times), the frequency of the vibrations follows the temperature distribution over time. In regions that cool down, the vibrations reduce as well (and vice versa).  

### Modelling the Vibrations
We model the vibrations by assuming that the frequency of oscillation around the equilibrium position, $\omega$, is proportional to the square root of temperature:
$$\omega(x,t) = \omega_0/3 + \omega_0\sqrt{u(x,t)}.$$
Note that since the temperature depends on space and time, the vibration frequency does so as well. This makes perfect sense in light of what we discussed previously: in hotter regions, the atoms oscillate faster in the lattice. The constant of proportionality is called $\omega_0$. In the calculations behind the animation (see [code](/fourier_solutions_heat_equation.py)), we always take $u\geq 0$ for calculational convenience. However, we do not use an absolute temperature scale (like Kelvins), so even at $u = 0$ the atoms still vibrate. Therefore we included a constant term $\omega_0/3$ to mimick this. In fact, the above equation is only dimensionally correct if the temperature is dimesionless. In fact, it should not be taken as a precise physical law, but merely as a functional relationship to used to make the relation between temperature and lattice vibrations clear in the animations. 

To add a bit of variaty, the atoms can vibrate in an arbitrary direction in the the 2D plane. Suppose the equilibrium position of the $i$-th atom in the lattice is given by $(x_\mathrm{eq}^{(i)}, y_\mathrm{eq}^{(i)})$ and the atom oscillates in a random direction $\theta^{(i)}\in[0,2\pi]$ with respect to the $x$-axis. Then the motion of the particle is given by:
```math
\begin{align*}
x^{(i)}(t) &= x^{(i)}_\mathrm{eq} + A\sin (\omega(x_\mathrm{eq}^{(i)}_\mathrm{eq},t)t)\cos\theta^{(i)} \nonumber\\
y^{(i)}(t) &= y^{(i)}_\mathrm{eq} + A\sin (\omega(x_\mathrm{eq}^{(i)}_\mathrm{eq},t)t)\sin\theta^{(i)} 
\end{align*}
```







## Dirichlet BCs
https://github.com/timdewild/heat-equation-rod/assets/93600756/b446ba26-cad3-4a81-be8a-be11a59d7828

## Neumann BCs
https://github.com/timdewild/heat-equation-rod/assets/93600756/5583de22-49f6-4746-984b-337138eda75c

