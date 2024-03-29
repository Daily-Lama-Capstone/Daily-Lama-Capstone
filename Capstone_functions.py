import pandas as pd
import sql_functions as sf


def df_main(xtree):
    result = []
    for node in xtree:
        try:
            id = node.attrib.get("objectid")
            yearpublished = node.find("yearpublished").text
            description = node.find("description").text
            minplayers = node.find("minplayers").text
            maxplayers = node.find("maxplayers").text
            playingtime = node.find("playingtime").text
            maxplayingtime = node.find("maxplaytime").text
            minplayingtime = node.find("minplaytime").text
            min_age = node.find("age").text
            result.append({"id": id ,"description": description, "yearpublished": yearpublished, 
                        "min_players": minplayers,"max_players": maxplayers, "playtime":playingtime, "min_playtime":minplayingtime, 
                        "max_playtime":maxplayingtime, "min_age": min_age})
        except:
            continue
    return pd.DataFrame(result)


def df_game_type(xtree):
    type_d = []
    for node in xtree:
        id = node.attrib.get("objectid")
    for node2 in node:
        if node2.tag == 'rpg':
            type_d.append({'id': id, 'type': 'rpg'})
        elif node2.tag == 'videogametheme':
            type_d.append({'id': id, 'type': 'videogame'})  
        else:
            type_d.append({'id': id, 'type': 'general'})  

    return pd.DataFrame(type_d).drop_duplicates()

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
                if 'primary' in node2.attrib:
                    primary_name = 1
                else:
                    primary_name = 0
                result.append({"id": id ,"name": node2.text,"primary": primary_name})
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

def rename_game_names(df,column_name="game_name"):
    if column_name in df.columns:
        df[column_name] =  df[column_name].str.findall(r'\w|\s').str.join('').str.replace(r"\s+","_").str.lower()
    return df

def avg_price_from_marketplace(query = f"Select * from bgg_data.marketplace_listings",
                                new = True, likenew = True, verygood = True):
    """ 
    Optional INPUT arguments: \n
    - query to get the dataframe from our db \n
    - new, likenew, verygood are the conditions. All are True by default. Set at least new=True\n\n
    OUTPUT:\n
    dataframe with only unique ids per row and average prices from input marketplace_listings dataframe
    """
    df = sf.get_dataframe(query)
    if new and likenew and verygood:
        mask = (df['condition'] == 'new') | ( df['condition'] == 'likenew') | (df["condition"] == "verygood")
    elif new and likenew:
        mask = (df['condition'] == 'new') | ( df['condition'] == 'likenew')
    elif new:
        mask = (df['condition'] == 'new')
    else:
        mask = (df == df)
    df_filter = df.where(mask)
    df_filter.dropna()
    df_avg_prices = df_filter.groupby('id').mean().reset_index()
    df_avg_prices["id"] = df_avg_prices["id"].convert_dtypes(convert_integer=True)
    df_avg_prices = df_avg_prices[["id","price_in_dollars"]]
    df_avg_prices.rename({"price_in_dollars":"avg_price"},axis=1,inplace=True)
    df_avg_prices["avg_price"] = df_avg_prices["avg_price"].round(2)
    return df_avg_prices