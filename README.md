# Heat Equation for 1-Dimensional Rod
In this animation (made using the [`matnimation`](https://github.com/timdewild/matnimation/tree/main) module), we model the cooling of a 1-dimensional metal rod, subject to different boundary conditions (BCs). 

## Solving the Heat Equation
We will solve the heat equation for a 1-dimensional metal rod of unit length. Of course, 1-dimensional rods do not exist, but this is a very good approximation for rods whose thickness $d$ is much smaller then their length $L$. The location along the rod is indicated by the the coordinate $x$. The temperature along the rod at a given moment in time $t$ is denoted by $u(x,t)$. 

The question we wish to answer is the following: given the temperature distribution along the rod at $t=0$, what will be the temperature distribution at all subsequent times $t>0$? 

The time-evolution of the temperature $u$ is given by a partial differential equation (PDE) called the heat equation:

$$u_t = D u_{xx},$$

where $D$ is the thermal diffusivity and subscripts denote partial derivatives with respect to the subscripted variable. To solve this PDE, we need two extra ingredients: initial and boundary conditions. We will work in units such that the bar has unit length and hence $x\in [0,1]$. 

### Initial Conditions
Initial conditions describe the state of the system at the initial time. In our case, this is the temperature distribution along the rod at time $t=0$, which we denote by $f(x)$. That is:

$$u(x,0)\equiv f(x), \quad x\in[0,1].$$





## Dirichlet BCs
https://github.com/timdewild/heat-equation-rod/assets/93600756/b446ba26-cad3-4a81-be8a-be11a59d7828

## Neumann BCs
https://github.com/timdewild/heat-equation-rod/assets/93600756/5583de22-49f6-4746-984b-337138eda75c

