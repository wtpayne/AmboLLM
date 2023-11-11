"""Welcome to Reflex!."""

from AmboLLM import styles

# Import all the pages.
from AmboLLM.pages import *

import reflex as rx

# Create the app and compile it.
app = rx.App(style=styles.base_style)
app.compile()
