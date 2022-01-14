# Theme-specific elements

There are a few elements that are unique or particularly important to this theme.
This page is a reference for how these look.

## Embedding in admonitions

````{note}
Here's a note with:

- A nested list
- List item two

As well as:

```{warning}
A nested warning block to test nested admonitions.
```
````

## Version changes

You can write in your documentation when something has been changed,
added or deprecated from one version to another.

```{versionadded} 0.1.1
Something is new, use it from now.
```

```{versionchanged} 0.1.1
Something is modified, check your version number.
```

```{deprecated} 0.1.1
Something is deprecated, use something else instead.
```

## HTML elements

There are some libraries in the PyData ecosystem that use HTML and require their own styling.
This section shows a few examples.

### Plotly

The HTML below shouldn't display, but it uses RequireJS to make sure that all
works as expected. If the widgets don't show up, RequireJS may be broken.

```{jupyter-execute}
import plotly.io as pio
import plotly.express as px
import plotly.offline as py

pio.renderers.default = "notebook"

df = px.data.iris()
fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species", size="sepal_length")
fig
```

### Xarray

Here we demonstrate `xarray` to ensure that it shows up properly.

```{jupyter-execute}
import xarray as xr
import numpy as np
data = xr.DataArray(
        np.random.randn(2, 3),
        dims=("x", "y"),
        coords={"x": [10, 20]}, attrs={"foo": "bar"}
      )
data
```
