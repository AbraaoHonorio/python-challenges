from payment_app.payment_app.domain.affiliation import Affiliation


class Member:
    def __init__(self, name: str, affiliation: Affiliation = None):
        self.name = name
        self.affiliation = affiliation

    def activate_affiliation(self, affiliation_type: str):
        self.affiliation = Affiliation(affiliation_type, True)
