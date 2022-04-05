import math
import numpy as np


class ConicSolver:
    def __init__(self) -> object:
        # instance attributes taken from tfocs_initialize.m
        self.max_iterations = float('inf')
        self.max_counts = float('inf')
        self.count_ops = False
        self.save_history = True
        self.adjoint = False
        self.saddle = False
        self.tolerance = 1e-8
        self.error_function = None
        self.stop_function = None
        self.print_every = 100
        self.max_min = 1
        self.beta = 0.5
        self.alpha = 0.9
        self.L_0 = 1
        self.L_exact = float('inf')
        self.mu = 0
        self.fid = 1
        self.stop_criterion = 1
        self.alg = 'AT'
        self.restart = float('inf')
        self.print_stop_criteria = False
        self.counter_reset = -50
        self.cg_restart = float('inf')
        self.cg_type = 'pr'
        self.stop_criterion_always_use_x = False
        self.data_collection_always_use_x = False
        self.output_always_use_x = False
        self.auto_restart = 'gra' # function or gradient
        self.print_restart = True
        self.debug = False


    def auslender_teboulle(self, smooth_func, affine_func, projector_func, x0):
        """Auslender & Teboulle's method
        args:
            smooth_func: function for smooth

        """
        alg = 'AT'

        # following taken from tfocs_initialize.m
        L = self.L_0
        theta = float('inf')
        f_v_old = float('inf')
        x = [] #FIXME: taken from matlab (TFOCS), should probably be number
        A_x = []
        f_x = float('inf')
        C_x = float('inf')
        g_x = []
        g_Ax = []
        restart_iter = 0
        warning_lipschitz = 0
        backtrack_simple = True
        backtrack_tol = 1e-10
        backtrack_steps = 0

        counter_Ay = 0
        counter_Ax = 0

        # iteration values
        y = x
        z = x
        A_y = A_x
        A_z = A_x
        C_y = float('inf')
        C_z = C_x
        f_y = f_x
        f_z = f_x
        g_y = g_x
        g_z = g_x
        g_Ay = g_Ax
        g_Az = g_Ax

        while True:
            x_old = x
            z_old = z
            A_x_old = A_x
            A_z_old = A_z

            # backtracking loop
            L_old = L
            L = L * self.alpha
            theta_old = theta

            #FIXME: theta is Inf
            while True:
                # acceleration
                theta = self.advance_theta(theta_old)

                # next iteration
                if theta < 1:
                    y = (1 - theta) * x_old + theta * z_old

                    if counter_Ay >= self.counter_reset:
                        A_y = apply_linear(y, 1)
                        counter_Ay = 0

                    else:
                        counter_Ay += 1
                        A_y = (1 - theta) * A_x_old + theta * A_z_old

                f_y = float('inf')
                g_Ay = [] # should be numpy array?
                g_y = [] # see above

        if g_y.empty():
            if g_Ay.empty():
                np.array[f_y, g_Ay] = apply_smooth(A_y)

            g_y = apply_linear(g_Ay, 2)

        step = 1 / (theta * L)
        C_z, z = apply_projector(z_old - step * g_y, step)
        A_z = apply_linear(z, 1)



    # assuming countOps (?), see tfocs_initialize.m line 398
    # TODO: remove varagin?
    def apply_projector(self, varargin, projector_function):
        if self.count_ops:
            TODO

        # false by default
        else:
            projector_function(varargin)


    def apply_linear(x, mode):
        return solver_apply(3, linear_function, x, mode)

    def solver_apply(self):
        TODO

    def linear_function(self):
        TODO


    # assumes mu > 0 & & ~isinf(Lexact) && Lexact > mu,
    # see tfocs_initialize.m (line 532-) and healernoninv.m
    def advance_theta(self, theta_old: float):

        # TODO: calculating this inside theta expensive. move outside
        ratio = math.sqrt(self.mu / self.L_exact)
        theta_scale = (1 - ratio) / (1 + ratio)
        return min(1.0, theta_old, theta_scale)
