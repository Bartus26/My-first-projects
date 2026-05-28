"""
The equation describing the curve is:
y(x) = a * cosh(x / a) - a

Where:

x — horizontal position along the span
a = H / w — catenary parameter
H — horizontal tension in the cable [kN]
w — cable weight per unit length [kN/m]
cosh — hyperbolic cosine (np.cosh)

"""
import numpy as np

class CatenaryCurve:
    def __init__(self,L,H,w,n=20):

        # Inputed parameters:
        self.L = L
        self.H = H
        self.w = w
        self.n = n 
        
        # calculated veriables:
            # Catenary parameter:
        self.a = self.H / self.w
            # Horizontal position - array
        self.x = np.linspace(0,self.L,n)
            # Vertical positions - array
        self.y = self.a * np.cosh(self.x/self.a) - self.a 
            # Tensions - array
        self.t = (self.y*self.w) + self.H  
            # Length of rope
        self.s = 2 * self.a * np.sinh(self.L / (2 * self.a))

    def catenry_parameter(self):
        print(f"Catenary parameter = {self.a:.2f}")
        
    def max_sag(self):
        sag = self.a*(np.cosh(self.L/(2*self.a))-1)
        print(f"Maximum sag = {sag:.2f} m")

    def cable_length(self):
        print(f"Total cable length = {self.s:.2f} m")

    def max_tension(self):
        t_max = np.max(self.t)
        t_max_ndx = np.argmax(self.t)
        print(f"\nMaximum tension in the cable = {t_max:.2f} kN")
        print(f"Maximum tension x coordinate = {self.x[t_max_ndx]} m")

    def exceed_tension(self,tnsn_brdr = 900):
        self.tnsn_brdr = tnsn_brdr
        t_excd_ind = np.where(self.t > self.tnsn_brdr)[0]
        print(f"\nPoint/s exceed {self.tnsn_brdr} kN:")
        for i in t_excd_ind:
            print(f"x position = {self.x[i]:.2f} -> tension = {self.t[i]:.2f} kN ")

    def summary_matrix(self):
        sum_mtrx = np.column_stack((self.x, self.y, self.t))
        sum_mtrx = np.round(sum_mtrx,decimals=2)
        print("\nFirst 5 x[m],y[m],T[kN] parameters:")
        print(sum_mtrx[0:5])
        print(f"\nLast 5 x[m],y[m],T[kN] parameters:")
        print(sum_mtrx[self.n-5:self.n+1])

    def check_length(self):
       
       x_lengths = []
       y_lengths = []

        # creating array with x,y lengths       
       dx = np.diff(self.x)
       dy = np.diff(self.y)  

       segments = np.column_stack((dx,dy))        
     
       integration = np.linalg.norm(segments,axis=1)
       sum_int = np.sum(integration)
       difference = sum_int - self.s
       print(f"Sum integration lengths = {sum_int:.2f} m. Difference is {difference:.2f} m ")      




# MAIN

 # Object: L=180m, H = 850 kN, w = 1,8 kN/m, n=200
catenary1 = CatenaryCurve(180,850,1.8,200)
# Body:
    # Printing catenary parameter
catenary1.catenry_parameter()
    # Printing maximum sag 
catenary1.max_sag()
    # Printing cable length
catenary1.cable_length()
    # Printing maximal tension an its position
catenary1.max_tension()
    # Printing tensions exceeds primary set to 900 kN
catenary1.exceed_tension()
    # Printing Ffirst 5 and last 5 position from stacking x,y,t array
catenary1.summary_matrix()
    # Bonus: Chceck length of rope by numerical integration
catenary1.check_length()