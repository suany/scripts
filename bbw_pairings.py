#!/usr/bin/env python3

from __future__ import print_function

assignments_2025 = [
  ("Lisa",),
  ("Steph", "Tracy", "Ken H",),
  ("Suan", "Peggy", "J.Bain",),
  ("Caroline", "Paul",),
  ("Diane M", "Ken K",),
  ("Gladys", "Leigh",),
  ("Courtney", "Caleb",),
  ("Ken H", "Deb",),
  ("Lisa", "Peggy",),
  ("Anna", "Tracy", "Ken H",),
  ("Brian", "Steph",),
  ("Jared", "Deb",),
  ("Suan", "Jill", "Jane B",),
  ("Suan",),
  ("Ken K", "Jill", "Jane B",),
  ("Suan", "Gladys", "Ken H",),
  ("Lisa", "Tracy",),
  ("Anna", "Ken H",),
  ("Diane M", "Ken K",),
  ("Brian", "Deb",),
  ("Caleb", "Courtney",),
  ("Steph", "J.Leff", "J.Bain",),
  ("Paul", "Peggy",),
  ("Anna", "Gladys",),
  ("Jared", "Meena",),
  ("Deb", "Leigh",),
  ("Diane M", "Ken K",),
  ("Stephanie", "Suan", "J.Bain",),
  ("Paul", "Beth",),
  ("Ken H", "Lisa",),
  ("Gladys", "Jill",),
  ("Caroline", "Anna", "Deb", "Suan",),
  ("Brian", "Beth",),
  ("Jared", "Peggy",),
  ("Meena",),
  ("Stephanie", "J.Leff",),
  ("Caroline", "Dick",),
  ("Ken H", "Gladys", "J.Leff",),
  ("Suan", "Jill", "J.Bain",),
  ("Lisa", "Peggy",),
  ("Diane M", "Ken K",),
  ("Suan", "Tracy",),
  ("Jared", "Dick", "J.Bain", "Jill",),
  ("Paul", "Marc",),
  ("Diane M", "Ken K", "Dick", "Leigh",),
  ("Stephanie", "Leigh", "J.Leff", "J.Bain",),
  ("Anna", "Beth",),
  ("Ken H", "Tracy",),
  ("Lisa", "Dick",),
  ("Gladys", "Caroline", "Suan",),
  ("Jared", "Tracy",),
  ("Paul", "J.Leff", "Maia",),
  ("Leigh", "Lisa", "K.Haas",),
  ("Beth", "J.Leff", "Suan",),
  ("Gladys", "Paul",),
  ("Ken H", "Deb", "Suan",),
  ("Meena", "Suan", "Anna", "D.Traina",),
  ("Caroline", "Peggy", "Ken H",),
  ("Jared", "Tracy", "J.Bain",),
  ("Diane M", "Ken K",),
  ("Beth", "Suan", "Shelley", "J.Bain",),
  ("Gladys", "Suan", "D.Traina", "J.Bain", "K.Haas",),
  ("Paul", "Maia",),
  ("Lisa", "Tracy", "D.Traina", "K.Haas",),
  ("Diane M", "Ken K", "BB",),
  ("Ken Haas", "Deb", "Janie",),
  ("Jared", "Peggy", "BB",),
  ("K.Haas", "Janie", "Suan",),
  ("Stephanie", "Leigh", "BB", "Suan",),
  ("Suan", "Tracy", "Anna", "Shelley",),
  ("Diane M", "K.Haas",),
  ("Beth", "Gladys", "Shelley",),
  ("Jared", "Stephanie", "BB", "Suan",),
  ("Caroline", "J.Leff",),
  ("Ken Haas", "Peggy",),
  ("Paul", "Leigh", "Maia",),
  ("Suan", "Dick", "BB", "J.Bain",),
  ("Lisa", "Deb", "K.Haas", "Shelley",),
  ("Paul", "Dick", "Tracy", "J.Bain", "Jill",),
  ("Gladys", "Peggy", "Suan", "J.Bain",),
  ("Diane M", "Ken K", "BB", "Beth", "Ken H",),
  ("Anna", "Shelley",),
  ("Diane T", "Suan",),
  ("Ken Haas", "Debbie",),
  ("Stephanie", "Maia", "K.Haas",),
  ("Beth", "Caroline", "K.Haas",),
  ("Lisa", "K.Haas", "J.Bain", "Suan",),
  ("Paul", "Shelley", "J.Bain", "Stephanie",),
  ("Ken Haas", "Ken K",),
  ("Ken Haas", "Tracy",),
  ("Beth", "Diane T", "K.Haas",),
  ("Gladys", "Debbie", "K.Haas",),
  ("Anna", "Jared", "K.Haas",),
  ("Stephanie", "Maia", "K.Haas",),
  ("Lisa", "Tracy", "K.Haas",),
  ("Paul", "Shelley", "K.Haas",),
  ("Beth", "Janie",),
  ("Ken Haas", "Debbie",),
  ("Diane T", "Gladys",),
  ("Diane M", "Ken K", "K.Haas",),
  ("Stephanie", "Janie",),
  ("Caroline", "Maia", "K.Haas",),
  ("Suan", "Tracy", "J.Bain",),
  ("Lisa", "Peggy", "K.Haas",),
  ]

leaders = (
  "Anna",
  "BB",
  "Beth",
  "Brian",
  "Caleb",
  "Caroline",
  "Courtney",
  "D.Morton",
  "D.Traina",
  "Debbie",
  "Dick",
  "Gladys",
  "J.Bain",
  "J.Leff",
  "Jared",
  "Jill",
  "K.Haas",
  "Ken K",
  "Leigh",
  "Lisa",
  "Maia",
  "Marc",
  "Meena",
  "Paul",
  "Peggy",
  "Shelley",
  "Stephanie",
  "Suan",
  "Tracy",
  )

aliases = {
  "Deb" : "Debbie",
  "Diane M" : "D.Morton",
  "Diane T" : "D.Traina",
  "Jane B" : "J.Bain",
  "Janie" : "J.Leff",
  "Ken H" : "K.Haas",
  "Ken Haas" : "K.Haas",
  "Steph" : "Stephanie",
}

class PairingInfo(object):
    def __init__(self):
        self.count = 0
        self.latest = None
    def update(self, age):
        self.count += 1
        if self.latest is None:
            self.latest = age
        else:
            assert age >= self.latest
    def __repr__(self):
        return f"cnt={self.count} latest={self.latest}"

pairings = dict() # name1 -> dict[name2 -> PairingInfo]

def process(n1, n2, age):
    pairing = pairings.setdefault(n1, dict())
    info = pairing.setdefault(n2, PairingInfo())
    info.update(age)

if __name__ == "__main__":
    for age, tup in enumerate(reversed(assignments_2025)):
        while len(tup) > 1:
            n1 = tup[0]
            nn1 = aliases.get(n1, n1)
            if not nn1 in leaders:
                print("Missing leader", nn1)
                assert False
            tup = tup[1:]
            for n2 in tup:
                nn2 = aliases.get(n2, n2)
                if not nn2 in leaders:
                    print("Missing leader", nn2)
                    assert False
                process(nn1, nn2, age)
                process(nn2, nn1, age)

    for n1 in sorted(pairings):
        n1pairings = pairings.get(n1)
        for n2 in sorted(n1pairings):
            print(n1, n2, n1pairings.get(n2))
