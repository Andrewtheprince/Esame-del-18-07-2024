from dataclasses import dataclass

@dataclass
class Gene:
    GeneID: str
    Chromosome: int
    Localization: str


    def __str__(self):
        return f"{self.GeneID} {self.Chromosome} {self.Localization}"

    def __hash__(self):
        return hash(self.GeneID)