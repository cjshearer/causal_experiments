import io
from matplotlib import pyplot as plt
import matplotlib.image as mpimg


# graph given dot file with graphviz and view with matplotlib
# https://stackoverflow.com/questions/40010237/python-plot-base64-string-as-image
def dot_to_matplotlib(dot):
  # https://graphviz.readthedocs.io/en/stable/api.html#graphviz.pipe
  i = dot.pipe(format="png")
  i = io.BytesIO(i)
  i = mpimg.imread(i, "png")

  plt.imshow(i, interpolation='nearest')
  plt.show()
