# Keyboard shortcuts

## Trigger the search bar

You can trigger the search bar pop-up with {kbd}`Ctrl`/{kbd}`⌘` + {kbd}`K`.

## Change pages

By default, you can move to the previous/next page using the {octicon}`arrow-left` (left arrow) and {octicon}`arrow-right` (right arrow) keys on a keyboard.
To disable this behavior, use the following configuration:

```py
html_theme_options = {
    "navigation_with_keys": False
}
```

```{attention}
Keep in mind that many readers use their keyboards and other assistive technology to interact with web documents. If you disable the keyboard navigation, you might be making your documentaion inaccessible to many readers.
```
