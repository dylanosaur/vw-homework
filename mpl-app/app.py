import tornado.ioloop
import tornado.web
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
import base64

class PlotHandler(tornado.web.RequestHandler):
    def get(self):
        # Create a new figure and canvas
        fig = Figure()
        canvas = FigureCanvas(fig)
        
        # Generate the plot
        ax = fig.add_subplot(1, 1, 1)
        x = [1, 2, 3, 4, 5]
        y = [3, 5, 2, 7, 4]
        ax.plot(x, y)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Plot Example')
        
        # Render the canvas to a string buffer
        buffer = io.BytesIO()
        canvas.print_png(buffer)
        
        # Encode the image data as Base64
        image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        # Set the appropriate headers
        self.set_header('Content-Type', 'text/html')
        
        # Render the HTML template and pass the plot image data
        self.render("plot.html", image_data=image_data)

def make_app():
    return tornado.web.Application([
        (r"/plot", PlotHandler),
    ], template_path="templates")

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
