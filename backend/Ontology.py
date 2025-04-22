from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal, XSD

# Definirea namespace-ului ontologiei
BG = Namespace("http://example.org/boardgames#")

g = Graph()

# Clase principale
classes = ["Game", "Mechanic", "Domain", "PlayerCount", "Duration", "Complexity"]

for cls in classes:
    g.add((BG[cls], RDF.type, OWL.Class))

# Proprietăți principale (data properties și object properties)
properties = {
    "hasMechanic": OWL.ObjectProperty,
    "hasDomain": OWL.ObjectProperty,
    "minPlayers": OWL.DatatypeProperty,
    "maxPlayers": OWL.DatatypeProperty,
    "playTime": OWL.DatatypeProperty,
    "recommendedAge": OWL.DatatypeProperty,
    "averageRating": OWL.DatatypeProperty,
    "complexityRating": OWL.DatatypeProperty,
    "publishedYear": OWL.DatatypeProperty,
    "ownedByUsers": OWL.DatatypeProperty,
    "ratedByUsers": OWL.DatatypeProperty,
}

for prop, prop_type in properties.items():
    g.add((BG[prop], RDF.type, prop_type))

# Salvare structură ontologie
g.serialize("data/boardgame_ontology.owl", format="xml")
