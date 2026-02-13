from matplotlib.figure import Figure
from io import BytesIO
import base64

# Using https://matplotlib.org/stable/gallery/user_interfaces/web_application_server_sgskip.html

class Colorfinity:
    # CONSTANTS
    SIZE = [12, 6]
    
    def time_scattered(x, y, name, y_name):
        # Create a figure
        my_fig = Figure(figsize=Colorfinity.SIZE)

        # Customize the axes
        my_axe = my_fig.subplots()
        my_axe.set_title(name)
        my_axe.set_ylabel(y_name)
        my_axe.set_xlabel("Date")

        # Create the plot
        my_axe.plot(x, y, color='magenta', marker='.', linestyle='None')

        # Then we convert the plot into nice bytes
        my_buf = BytesIO()
        my_fig.savefig(my_buf, format="png")
        my_data = base64.b64encode(my_buf.getbuffer()).decode("ascii")
        # Done
        return my_data

        
