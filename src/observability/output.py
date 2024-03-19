# %pip install trulens

import torch
from trulens.visualizations import HTML, IPython, Output


class GradioHTML(Output):
    """Gradio Highligher visualization output format."""

    def __init__(self):
        super().__init__()

    def blank(self):
        return []

    def space(self):
        return " "

    def escape(self, s):
        return s

    def linebreak(self):
        return "\n"

    def line(self, s):
        return s

    def clean(self, s):
        return s.replace(" ", "")

    def magnitude_colored(self, s, mag):
        return (self.clean(s), round(torch.Tensor.item(mag), 3) * 100)

    def append(self, *pieces) -> list:
        # firs case: label
        if len(pieces) == 3 and pieces[1] == ":" and pieces[2] == self.space():
            return [pieces[0]]

        # second case: append space
        elif len(pieces) == 2 and pieces[1] == self.space():
            return pieces[0]

        # third case: list = list + new tuple
        elif len(pieces) == 2:
            pieces[0].append(pieces[1])
            return pieces[0]

        # fourth case: add contents
        elif len(pieces) == 4:
            # (first time : blank + new content + br + br )
            if pieces[0] == self.blank():
                return pieces[1]
            # (nth time : content + new content + br + br )
            else:
                return [pieces[0], pieces[1]]

        return pieces

    def render(self, s):

        return s


class CustomHTML(HTML):
    """Interactive python visualization output format."""

    def __init__(self):
        super().__init__()

    def clean(self, s):
        return s.replace(" ", "")

    def magnitude_colored(self, s, mag):
        red = 0.0
        green = 0.0
        if mag > 0:
            green = 1.0  # 0.5 + mag * 0.5
            red = 1.0 - mag * 0.5
        else:
            red = 1.0
            green = 1.0 + mag * 0.5
            # red = 0.5 - mag * 0.5

        blue = min(red, green)
        # blue = 1.0 - max(red, green)

        return f"<span title='{mag:0.3f}' style='margin: 1px; padding: 1px; border-radius: 4px; background: grey; color: rgb({red*255}, {green*255}, {blue*255});'>{self.clean(s)}</span>"


class CustomIPython(IPython):
    """Interactive python visualization output format."""

    def __init__(self):
        super().__init__()

    def clean(self, s):
        return s.replace(" ", "")

    def magnitude_colored(self, s, mag):
        red = 0.0
        green = 0.0
        if mag > 0:
            green = 1.0  # 0.5 + mag * 0.5
            red = 1.0 - mag * 0.5
        else:
            red = 1.0
            green = 1.0 + mag * 0.5
            # red = 0.5 - mag * 0.5

        blue = min(red, green)
        # blue = 1.0 - max(red, green)

        return f"<span title='{mag:0.3f}' style='margin: 1px; padding: 1px; border-radius: 4px; background: grey; color: rgb({red*255}, {green*255}, {blue*255});'>{self.clean(s)}</span>"
