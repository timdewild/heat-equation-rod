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
$$u(x,t) = a_0+\sum_{n=1}^\infty b_n e^{-\lambda_n^2 t}\cos(\mu_n x),$$ where the coefficients $a_n$ are the sine Fourier coefficients: $$a_0 = \int_0^1 dx\\; f(x),\quad a_n = 2\int_0^1 dx\\; f(x)\cos(\mu_n x).$$ Note that the coefficient $a_0$ is the average of the initial temperature distribution $f(x)$:
$$a_0 = \bar{f}.$$ As $t\to\infty$, the solution asymptotes to $u(x,t)\to a_0$. This is to be expected, since the bar is insulated and the thermal energy distributes evenly over the bar so that the rod acquires a constant temperature everywhere. It is not suprising that this temperature is equal to the average of the initial temperature profile. 







## Dirichlet BCs
https://github.com/timdewild/heat-equation-rod/assets/93600756/b446ba26-cad3-4a81-be8a-be11a59d7828

## Neumann BCs
https://github.com/timdewild/heat-equation-rod/assets/93600756/5583de22-49f6-4746-984b-337138eda75c

