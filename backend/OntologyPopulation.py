import json
from rdflib import Graph, Namespace, RDF, RDFS, Literal, XSD

g = Graph()
g.parse("../onto/boardgame_ontology.owl", format="xml")

BG = Namespace("http://example.org/boardgames#")

def normalize_uri(value):
    import re
    return re.sub(r'\W+', '_', value.strip())

with open("../data/combined_boardgames.json", encoding="utf-8") as f:
    games = json.load(f)

def classify_playercount(min_players):
    if int(min_players) == 1:
        return "Solo"
    elif int(min_players) == 2:
        return "Couple"
    elif 3 <= int(min_players) <= 5:
        return "Group"
    elif int(min_players) >= 6:
        return "Party"
    return None

def classify_duration(time):
    if int(time) <= 30:
        return "Short"
    elif 31 <= int(time) <= 90:
        return "Medium"
    elif 91 <= int(time) <= 180:
        return "Long"
    elif int(time) > 180:
        return "Epic"
    return None

def classify_complexity(value):
    if float(value) <= 1.5:
        return "Very_Easy"
    elif 1.5 < float(value) <= 2.5:
        return "Easy"
    elif 2.5 < float(value) <= 3.5:
        return "Medium"
    elif float(value) > 3.5:
        return "Hard"
    return None

for game in games:
    game_uri = BG[f'Game_{game["id"]}']
    g.add((game_uri, RDF.type, BG.Game))
    g.add((game_uri, RDFS.label, Literal(game["title"], datatype=XSD.string)))

    year_raw = game.get("year", "")
    year_int = int(year_raw)
    if 1000 <= year_int <= 9999:
        year_str = f"{year_int:04d}"
        g.add((game_uri, BG.publishedYear, Literal(year_str, datatype=XSD.gYear)))
    if game["minplayers"]:
        g.add((game_uri, BG.minPlayers, Literal(int(game["minplayers"]), datatype=XSD.integer)))
    if game["maxplayers"]:
        g.add((game_uri, BG.maxPlayers, Literal(int(game["maxplayers"]), datatype=XSD.integer)))
    if game["playingtime"]:
        g.add((game_uri, BG.playTime, Literal(int(game["playingtime"]), datatype=XSD.integer)))
    if game["minage"]:
        g.add((game_uri, BG.recommendedAge, Literal(int(game["minage"]), datatype=XSD.integer)))
    if game["avg_rating"]:
        g.add((game_uri, BG.averageRating, Literal(float(game["avg_rating"]), datatype=XSD.float)))
    if game["weight"]:
        g.add((game_uri, BG.complexityRating, Literal(float(game["weight"]), datatype=XSD.float)))

    for mech in set(game.get("mechanics", [])):
        mech_name = normalize_uri(mech)
        mech_uri = BG[f'Mechanic_{mech_name}']
        g.add((mech_uri, RDF.type, BG.Mechanic))
        g.add((mech_uri, RDFS.label, Literal(mech.strip(), datatype=XSD.string)))
        g.add((game_uri, BG.hasMechanic, mech_uri))

    for domain in set(game.get("categories", [])):
        domain_name = normalize_uri(domain)
        domain_uri = BG[f'Domain_{domain_name}']
        g.add((domain_uri, RDF.type, BG.Domain))
        g.add((domain_uri, RDFS.label, Literal(domain.strip(), datatype=XSD.string)))
        g.add((game_uri, BG.hasDomain, domain_uri))

    for designer in set(game.get("designers", [])):
        designer_name = normalize_uri(designer)
        designer_uri = BG[f"Designer_{designer_name}"]
        g.add((designer_uri, RDF.type, BG.Designer))
        g.add((designer_uri, RDFS.label, Literal(designer, datatype=XSD.string)))
        g.add((game_uri, BG.hasDesigner, designer_uri))

    for exp in game.get("has_expansions", []):
        if isinstance(exp, dict) and 'id' in exp and 'title' in exp:
            exp_uri = BG[f"Game_{exp['id']}"]
            g.add((game_uri, BG.hasExpansion, exp_uri))
            g.add((exp_uri, RDF.type, BG.Game))
            g.add((exp_uri, RDFS.label, Literal(exp["title"], datatype=XSD.string)))

    for expanded_game in game.get("expands", []):
        if isinstance(expanded_game, dict) and 'id' in expanded_game:
            expanded_uri = BG[f"Game_{expanded_game['id']}"]
            g.add((game_uri, BG.isExpansionOf, expanded_uri))

    pcat = classify_playercount(game.get("minplayers", 0))
    if pcat:
        g.add((game_uri, BG.hasPlayerCountCategory, BG[pcat]))

    dcat = classify_duration(game.get("playingtime", 0))
    if dcat:
        g.add((game_uri, BG.hasDurationCategory, BG[dcat]))

    ccat = classify_complexity(game.get("weight", 0))
    if ccat:
        g.add((game_uri, BG.hasComplexityCategory, BG[ccat]))

output_path = "../onto/boardgame_ontology_populated_json.owl"
print(len(g))
g.serialize(output_path, format="xml")
