import numpy as np

class FourierHeatSolution:
    def __init__(
            self, 
            x_array: np.ndarray, 
            t_array: np.ndarray, 
            fourier_coeff: callable, 
            boundary_cond: str = 'dirichlet', 
            diffusivity: float = 1, 
            number_of_terms: int = 30
            ):
        
        self.x_array = x_array
        self.t_array = t_array
        self.fourier_coeff = fourier_coeff
        self.boundary_cond = boundary_cond
        self.diffusivity = diffusivity
        self.number_of_terms =  number_of_terms

        self.c = np.sqrt(self.diffusivity)
        self.Nx, self.Nt = len(self.x_array), len(self.t_array)
        self.temperature_grid = None
        self.heat_flux_grid = None

    def _mu(self, n: int):
        return n * np.pi
    
    def _lam(self, n: int):
        return self.c * n * np.pi
    
    def _normal_mode_temp(self, x, t, n: int):
        if self.boundary_cond == 'dirichlet':
            return self.fourier_coeff(n) * np.exp(-self._lam(n) ** 2 * t) * np.sin(self._mu(n) * x)
        
        if self.boundary_cond == 'neumann':
            return self.fourier_coeff(n) * np.exp(-self._lam(n) ** 2 * t) * np.cos(self._mu(n) * x)
        
    def _normal_mode_flux(self, x, t, n: int):
        if self.boundary_cond == 'dirichlet':
            return -self._mu(n) * self.fourier_coeff(n) * np.exp(-self._lam(n) ** 2 * t) * np.cos(self._mu(n) * x)
        
        if self.boundary_cond == 'neumann':
            return +self._mu(n) * self.fourier_coeff(n) * np.exp(-self._lam(n) ** 2 * t) * np.sin(self._mu(n) * x)
    
    def temperature(self, x, t):
        temp = 0

        for n in range(1, self.number_of_terms + 1):
            temp += self._normal_mode_temp(x, t, n)

        # add constant term a0 to temperature
        if self.boundary_cond == 'neumann':
            temp += self.fourier_coeff(0)
        
        return temp
    
    def heat_flux(self, x, t):
        flux = 0

        for n in range(1, self.number_of_terms + 1):
            flux += self._normal_mode_flux(x, t, n)

        return flux

    def temperature_evo(self):
        """Rows: x-values, Cols: t-values."""

        x = self.x_array[:, np.newaxis]
        t = self.t_array[np.newaxis, :]

        self.temperature_grid = self.temperature(x, t)

        return self.temperature_grid
    
    def temperature_grid_evo(self, X, Y, t):
        return self.temperature(x = X, t = t)
    
    def heat_flux_evo(self, x: np.ndarray = None, t: np.ndarray = None):
        """Rows: x-values, Cols: t-values."""

        if (x is not None) and (t is not None):
            x = x[:, np.newaxis]
            t = t[np.newaxis, :]

        else:
            x = self.x_array[:, np.newaxis]
            t = self.t_array[np.newaxis, :]

        self.heat_flux_grid = self.heat_flux(x, t)

        return self.heat_flux_grid
    
    def omega(self, x, t, omega0 = 1):
        return omega0 / 3 + omega0 * (self.temperature(x,t)) ** 0.5
        



        


        