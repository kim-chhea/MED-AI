class Drug:
    def __init__(self, name, side_effects=None):
        self.name = name
        self.side_effects = side_effects if side_effects is not None else []

    def add_side_effect(self, side_effect):
        if side_effect not in self.side_effects:
            self.side_effects.append(side_effect)

    def __repr__(self):
        return f"Drug(name={self.name}, side_effects={self.side_effects})"