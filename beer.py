"""Module containting beer class definition"""
class Beer:
    """Class representing a beer"""
    def __init__(self, name, style, abv: float, info):
        self.name = name
        self.style = style
        self.abv = abv
        self.info = info

    def __lt__(self, other):
        return self.abv < other.abv

    def get_name(self):
        """Get the name of a beer."""
        return self.name
