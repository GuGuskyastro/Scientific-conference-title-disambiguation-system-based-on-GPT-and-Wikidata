'''
Created on 2023-06-22

@author: wf
'''
from nicegui import ui


class DictEdit:
    """
    User interface for dictionary editing

    using
        https://nicegui.io/documentation/tree

    """

    def __init__(self, card, d):
        """
        constructor
        """
        self.d = d
        with card:
            if d:
                for k in d.keys():
                    value = d[k]
                    ui.input(label=k,
                             value=str(value),
                             on_change=self.on_input_change).props("size=75")

    def on_input_change(self, event):
        """
        change the given value
        """
        pass
