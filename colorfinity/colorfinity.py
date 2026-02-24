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
        #my_axe.set_xticks([i*100 for i in range(len(x)//100)])

        # Create the plot
        my_axe.scatter(x, y, c=y, marker='.', linestyle='None')

        # Then we convert the plot into nice bytes
        my_buf = BytesIO()
        my_fig.savefig(my_buf, format="png")
        my_data = base64.b64encode(my_buf.getbuffer()).decode("ascii")
        
        # Done
        return my_data

    def time_boxplot(y_stats, title, y_label):
        # Create a figure
        my_fig = Figure(figsize=Colorfinity.SIZE)

        # Customize the axes
        my_axe = my_fig.subplots()
        my_axe.set_title(title)
        my_axe.set_ylabel(y_label)
        my_axe.set_xlabel("Date")

        # Create the plot
        my_axe.bxp(y_stats, showfliers=False)

        # Then we convert the plot into nice bytes
        my_buf = BytesIO()
        my_fig.savefig(my_buf, format="png")
        my_data = base64.b64encode(my_buf.getbuffer()).decode("ascii")

        return my_data
