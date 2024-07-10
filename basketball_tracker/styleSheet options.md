# PyQt6 Styling and ShadowLabel Example

## Common PyQt6 Options and Parameters

| Property                   | Description                                                                                         | Example Usage                                      |
|----------------------------|-----------------------------------------------------------------------------------------------------|----------------------------------------------------|
| `color`                    | Sets the text color.                                                                                | `color: red;`                                      |
| `background-color`         | Sets the background color.                                                                          | `background-color: blue;`                          |
| `font-family`              | Sets the font family.                                                                               | `font-family: Arial, sans-serif;`                  |
| `font-size`                | Sets the font size.                                                                                 | `font-size: 14px;`                                 |
| `font-weight`              | Sets the font weight (boldness).                                                                    | `font-weight: bold;`                               |
| `font-style`               | Sets the font style (e.g., italic).                                                                 | `font-style: italic;`                              |
| `text-decoration`          | Adds decoration to text (e.g., underline).                                                          | `text-decoration: underline;`                      |
| `border`                   | Sets the border around an element.                                                                  | `border: 1px solid black;`                         |
| `border-radius`            | Rounds the corners of an element.                                                                   | `border-radius: 5px;`                              |
| `padding`                  | Sets the padding inside an element.                                                                 | `padding: 10px;`                                   |
| `margin`                   | Sets the margin outside an element.                                                                 | `margin: 5px;`                                     |
| `width`                    | Sets the width of an element.                                                                       | `width: 100px;`                                    |
| `height`                   | Sets the height of an element.                                                                      | `height: 50px;`                                    |
| `min-width`                | Sets the minimum width of an element.                                                               | `min-width: 50px;`                                 |
| `min-height`               | Sets the minimum height of an element.                                                              | `min-height: 30px;`                                |
| `max-width`                | Sets the maximum width of an element.                                                               | `max-width: 200px;`                                |
| `max-height`               | Sets the maximum height of an element.                                                              | `max-height: 100px;`                               |
| `background-image`         | Sets a background image.                                                                            | `background-image: url('image.png');`              |
| `background-repeat`        | Sets if/how the background image is repeated.                                                       | `background-repeat: no-repeat;`                    |
| `background-position`      | Sets the starting position of a background image.                                                   | `background-position: center;`                     |
| `background-attachment`    | Sets whether a background image is fixed or scrolls with the rest of the page.                      | `background-attachment: fixed;`                    |
| `opacity`                  | Sets the opacity of an element.                                                                     | `opacity: 0.5;`                                    |
| `text-align`               | Sets the horizontal alignment of text.                                                              | `text-align: center;`                              |
| `vertical-align`           | Sets the vertical alignment of text.                                                                | `vertical-align: middle;`                          |
| `line-height`              | Sets the height of a line box.                                                                      | `line-height: 1.5;`                                |
| `letter-spacing`           | Sets the space between characters.                                                                  | `letter-spacing: 2px;`                             |
| `word-spacing`             | Sets the space between words.                                                                       | `word-spacing: 4px;`                               |
| `box-shadow`               | Adds shadow to an element.                                                                          | `box-shadow: 2px 2px 5px grey;`                    |
| `text-shadow`              | Adds shadow to text.                                                                                | `text-shadow: 1px 1px 2px black;`                  |
| `cursor`                   | Specifies the type of cursor to be displayed.                                                       | `cursor: pointer;`                                 |
| `transition`               | Adds transition effects to a property change.                                                       | `transition: all 0.3s ease-in-out;`                |
| `animation`                | Adds animation effects to an element.                                                               | `animation: mymove 5s infinite;`                   |
| `transform`                | Applies a 2D or 3D transformation to an element.                                                    | `transform: rotate(45deg);`                        |
| `display`                  | Specifies the display behavior of an element.                                                       | `display: block;`                                  |
| `position`                 | Specifies the positioning method used for an element.                                               | `position: absolute;`                              |
| `top`, `right`, `bottom`, `left` | Specifies the positioning of an element (used with `position` property).                     | `top: 10px;`                                       |
| `z-index`                  | Specifies the stack order of an element.                                                            | `z-index: 10;`                                     |
| `overflow`                 | Specifies what happens if content overflows an element's box.                                       | `overflow: hidden;`                                |

## Example Usage in PyQt6

To apply these styles in PyQt6, you can use the `setStyleSheet` method of your widget. Here’s an example of how you might use some of these properties in a PyQt6 application:

```python
from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout, QApplication
from PyQt6.QtCore import Qt
import sys

class ShadowLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)

    def enterEvent(self, event):
        self.setStyleSheet("""
            QLabel {
                color: yellow;
                background-color: black;
                border: 1px solid red;
                font-weight: bold;
                font-size: 16px;
                text-align: center;
                padding: 10px;
                border-radius: 5px;
                box-shadow: 2px 2px 5px grey;
                cursor: pointer;
            }
        """)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet("""
            QLabel {
                color: white;
                background-color: transparent;
                border: none;
                font-weight: bold;
                font-size: 14px;
                text-align: center;
                padding: 5px;
                border-radius: 3px;
            }
        """)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.setStyleSheet("""
       
