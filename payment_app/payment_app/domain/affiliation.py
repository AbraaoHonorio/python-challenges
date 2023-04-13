class Affiliation:
    def __init__(self, affiliation_type: str,
                 is_active: bool | None = False):
        self.affiliation_type = affiliation_type
        self.is_active = is_active

    def active(self):
        self.is_active = True

    def inactive(self):
        self.is_active = False
