from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal, XSD

BG = Namespace("http://example.org/boardgames#")
g = Graph()

classes = [
    "Game", "Mechanic", "Domain",
    "PlayerCountCategory", "DurationCategory", "ComplexityCategory", "Designer"
]

for cls in classes:
    g.add((BG[cls], RDF.type, OWL.Class))

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
    "hasPlayerCountCategory": OWL.ObjectProperty,
    "hasDurationCategory": OWL.ObjectProperty,
    "hasComplexityCategory": OWL.ObjectProperty,
    "hasDesigner": OWL.ObjectProperty,
    "hasExpansion": OWL.ObjectProperty,
    "isExpansionOf": OWL.ObjectProperty
}

for prop, prop_type in properties.items():
    g.add((BG[prop], RDF.type, prop_type))
    g.add((BG[prop], RDFS.label, Literal(prop.replace("_", " "), datatype=XSD.string)))

player_count_categories = ["Solo", "Couple", "Group", "Party"]
for category in player_count_categories:
    uri = BG[category]
    g.add((uri, RDF.type, BG.PlayerCountCategory))
    g.add((uri, RDFS.label, Literal(category)))

duration_categories = ["Short", "Medium", "Long", "Epic"]
for category in duration_categories:
    uri = BG[category]
    g.add((uri, RDF.type, BG.DurationCategory))
    g.add((uri, RDFS.label, Literal(category)))

complexity_categories = ["Very_Easy", "Easy", "Medium", "Hard"]
for category in complexity_categories:
    uri = BG[category]
    g.add((uri, RDF.type, BG.ComplexityCategory))
    g.add((uri, RDFS.label, Literal(category.replace("_", " "))))

g.serialize("../onto/boardgame_ontology.owl", format="xml")
