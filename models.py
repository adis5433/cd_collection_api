import json


class CDS:
    def __init__(self):
        try:
            with open("cds.json", "r") as f:
                self.cds = json.load(f)
        except FileNotFoundError:
            self.cds = []

        try:
            with open("favorites_cds.json", "r") as f:
                self.favorites_cds = json.load(f)
        except FileNotFoundError:
            self.favorites_cds = []

    def all(self):
        return self.cds

    def get(self, id):
        cd = [cd for cd in self.all() if cd['id'] == id]
        if cd:
            return cd[0]
        return []

    def create(self, data):
        self.cds.append(data)
        self.save_all()

    def save_all(self):
        with open("cds.json", "w") as f:
            json.dump(self.cds, f)

    def update(self, id, data):
        cd = self.get(id)
        if cd:
            index = self.cds.index(cd)
            self.cds[index] = data
            self.save_all()
            return True
        return False

    def add_favorites(self, id):
        cd = self.get(id)
        if cd:
            index = self.cds.index(cd)
            self.favorites_cdss.append(cds[index])
            with open("favorites_cds.json", "w") as f:
                json.dump(self.favorites_cds, f)

    def favorites(self):
        return self.favorites_cds





cds = CDS()