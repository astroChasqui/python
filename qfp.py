from bokeh.plotting import ColumnDataSource, figure, output_notebook, show
from bokeh.models import HoverTool
from collections import OrderedDict

def plot(x, y, labels=None, **kwargs):
    TOOLS="pan,wheel_zoom,box_zoom,reset,hover"
    p = figure(tools=TOOLS, **kwargs)
    try:
        l = list(labels)
    except:
        l = list(x)
    source = ColumnDataSource(
        data=dict(
            x = x,
            y = y,
            l = l,
        )
    )
    p.scatter(x, y, size=10, source=source)
    hover = p.select(dict(type=HoverTool))
    hover.tooltips = OrderedDict([
        ("Label", "@l"),
        ("X", "@x"),
        ("Y", "@y"),
    ])
    output_notebook()
    show(p)
