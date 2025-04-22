import pandas as pd
from rdflib import Graph, Namespace, RDF, Literal, XSD, URIRef, RDFS

# Încărcare structură ontologie existentă
g = Graph()
g.parse("data/boardgame_ontology.owl", format="xml")

BG = Namespace("http://example.org/boardgames#")

# Citire dataset
df = pd.read_csv("../data/BGG_Data_Set.csv", encoding="latin1")

for idx, row in df.iterrows():
    game_uri = BG[f'Game_{row["ID"]}']

    # Adăugare individ joc
    g.add((game_uri, RDF.type, BG.Game))
    g.add((game_uri, RDFS.label, Literal(row["Name"], datatype=XSD.string)))

    # Proprietăți simple
    g.add((game_uri, BG.publishedYear, Literal(row["Year Published"], datatype=XSD.gYear)))
    g.add((game_uri, BG.minPlayers, Literal(row["Min Players"], datatype=XSD.integer)))
    g.add((game_uri, BG.maxPlayers, Literal(row["Max Players"], datatype=XSD.integer)))
    g.add((game_uri, BG.playTime, Literal(row["Play Time"], datatype=XSD.integer)))
    g.add((game_uri, BG.recommendedAge, Literal(row["Min Age"], datatype=XSD.integer)))
    g.add((game_uri, BG.averageRating, Literal(row["Rating Average"], datatype=XSD.float)))
    g.add((game_uri, BG.complexityRating, Literal(row["Complexity Average"], datatype=XSD.float)))
    g.add((game_uri, BG.ownedByUsers, Literal(row["Owned Users"], datatype=XSD.integer)))
    g.add((game_uri, BG.ratedByUsers, Literal(row["Users Rated"], datatype=XSD.integer)))

    # Proprietăți multiple (Mechanics și Domains)
    if isinstance(row["Mechanics"], str):
        mechanics = row["Mechanics"].split(",")
        for mech in mechanics:
            mech_name = mech.strip().replace(" ", "_").replace("/", "_").replace("-", "_")
            mech_uri = BG[f'Mechanic_{mech_name}']
            g.add((mech_uri, RDF.type, BG.Mechanic))
            g.add((mech_uri, RDFS.label, Literal(mech.strip(), datatype=XSD.string)))
            g.add((game_uri, BG.hasMechanic, mech_uri))

    if isinstance(row["Domains"], str):
        domains = row["Domains"].split(",")
        for domain in domains:
            domain_name = domain.strip().replace(" ", "_").replace("/", "_").replace("-", "_")
            domain_uri = BG[f'Domain_{domain_name}']
            g.add((domain_uri, RDF.type, BG.Domain))
            g.add((domain_uri, RDFS.label, Literal(domain.strip(), datatype=XSD.string)))
            g.add((game_uri, BG.hasDomain, domain_uri))

# Salvare ontologie populată
g.serialize("data/boardgame_ontology_populated.owl", format="xml")
