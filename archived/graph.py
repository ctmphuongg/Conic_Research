import sage

# Define the variables
var('x y')

# Define the equation
eq = x**2 + 3*y**2 == 4

# Create the implicit plot
p = implicit_plot(eq, (x, -4, 4), (y, -4, 4), axes=True)

# Set the aspect ratio to 'equal' for a true circular appearance
p.set_aspect_ratio(1)

# Add labels and title
# p.set_xlabel('x')
# p.set_ylabel('y')
# p.set_title('Plot of x^2 + 3y^2 = 4')
show(p)
