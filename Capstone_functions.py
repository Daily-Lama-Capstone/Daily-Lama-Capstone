import pandas as pd


def df_main(xtree):
    result = []
    for node in xtree:
        id = node.attrib.get("objectid")
        description = node.find("description").text
        yearpublished = node.find("yearpublished").text
        minplayers = node.find("minplayers").text
        maxplayers = node.find("maxplayers").text
        playingtime = node.find("playingtime").text
        maxplayingtime = node.find("maxplaytime").text
        minplayingtime = node.find("minplaytime").text
        min_age = node.find("age").text
        result.append({"id": id ,"description": description, "yearpublished": yearpublished, 
                    "min_players": minplayers,"max_players": maxplayers, "playtime":playingtime, "min_playtime":minplayingtime, 
                    "max_playtime":maxplayingtime, "min_age": min_age})
    return pd.DataFrame(result)

def df_poll(xtree, entrypoint=""):
    '''
    INPUT:\n
    parser = lxml.etree.XMLParser(recover=True)\n 
    xtree = lxml.etree.parse("sample.xml", parser= parser).getroot()\n 
    entrypoint in ['suggested_numplayers', 'suggested_playerage', 'language_dependence']\n  
    OUTPUT:\n
    pandas.DataFrame
    '''
    result = []
    for node in xtree:
        id = node.attrib.get("objectid")
        for node3 in node.findall('poll'):
            for node4 in node3:
                for node5 in node4:
                    node_name = node3.attrib['name']
                    if node_name == "suggested_numplayers" and node5.attrib['numvotes'] != "0":
                        result.append({"id": id , "type_poll": node_name, "poll_value": node5.attrib['value'] + " for " + node4.attrib["numplayers"] + " player(s)", "num_votes": node5.attrib['numvotes']})
                    elif node_name == 'suggested_playerage' and node5.attrib['numvotes'] != "0":
                        result.append({"id": id , "type_poll": node_name, "poll_value": node5.attrib['value'], "num_votes": node5.attrib['numvotes']})
                    elif node_name == 'language_dependence' and node5.attrib['numvotes'] != "0":
                        result.append({"id": id , "type_poll": node_name, "poll_value": node5.attrib['value'], "num_votes": node5.attrib['numvotes']})
    return pd.DataFrame(result)


def df_subnodes(xtree, entrypoint="name"):
    '''
    INPUT:\n
    parser = lxml.etree.XMLParser(recover=True)\n 
    xtree = lxml.etree.parse("sample.xml", parser= parser).getroot()\n 
    entrypoint in [
        'boardgamecategory',
        'boardgamesubdomain',
        'boardgamemechanic',
        'boardgamefamily',
        'boardgameexpansion',
        'boardgamehonor',
        'boardgamedesigner',
        'boardgameartist',
        'boardgamepublisher',
        'boardgamepodcastepisode',
        'boardgameimplementation',
        'videogamebg',
        'statistics',
        'marketplacelistings'
    ]\n
    OUTPUT:\n
    pandas.DataFrame
    '''
    result = []
    subnodes = [
        'boardgamecategory',
        'boardgamemechanic',
        'boardgamefamily',
        'boardgameexpansion',
        'boardgamehonor',
        'boardgamedesigner',
        'boardgameartist',
        'boardgamepublisher',
        'boardgamepodcastepisode',
        'boardgameimplementation',
        'videogamebg',
        'boardgamesubdomain'
    ]
    for node in xtree:
        id = node.attrib.get("objectid")
        if entrypoint == "name":
            for node2 in node.findall('name'):
                result.append({"id": id ,"name": node2.text})
        elif entrypoint in subnodes:
            for node2 in node.findall(entrypoint):
                result.append({"id": id ,"cat_id": node2.attrib['objectid'] ,"cat_name": node2.text})
        elif entrypoint == "statistics":
            for node2 in node.findall(entrypoint):
                for node3 in node2:
                        result.append({"id": id, 
                        "average": node3.find("average").text,
                        "user_rated": node3.find("usersrated").text,
                        "num_owned": node3.find("owned").text,
                        "trading": node3.find("trading").text,
                        "wanting": node3.find("wanting").text,
                        "wishing": node3.find("wishing").text,
                        "numcomments": node3.find("numcomments").text,
                        "numweights": node3.find("numweights").text,
                        "averageweight": node3.find("averageweight").text,
                        })
        elif entrypoint == 'marketplacelistings':
            for node2 in node.findall(entrypoint):
                for node3 in node2:
                        result.append({
                        "id": id, 
                        "listdate": node3.find("listdate").text,
                        "price": node3.find("price").text,
                        "currency": node3.find("price").get("currency"),
                        "condition": node3.find("condition").text
                        })
    return pd.DataFrame(result)