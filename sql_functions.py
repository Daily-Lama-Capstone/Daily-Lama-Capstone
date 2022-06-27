# We import a method from the  modules to address environment variables and 
# we use that method in a function that will return the variables we need from .env 
# to a dictionary we call sql_config

from dotenv import dotenv_values

def get_sql_config():
    '''
        Function loads credentials from .env file and
        returns a dictionary containing the data needed for sqlalchemy.create_engine()
    '''
    needed_keys = ['host', 'port', 'database','user','password']
    dotenv_dict = dotenv_values(".env")
    sql_config = {key:dotenv_dict[key] for key in needed_keys if key in dotenv_dict}
    return sql_config

# Import sqlalchemy and pandas - do this only when instructed
import sqlalchemy
import pandas as pd

# Insert the get_data() function definition below - do this only when instructed in the notebook

def get_data(query):
    ''' Connect to the PostgreSQL database server, run query and return data'''
    # get the connection configuration dictionary using the get_sql_config function
    config = get_sql_config()
    # create a connection engine to the PostgreSQL server
    engine = sqlalchemy.create_engine('postgresql://user:pass@host/database',
                        connect_args=config # use dictionary with config details
                        )
    # open a conn session using 'with', execute the query, and return the results
    with engine.begin() as conn:
        results = conn.execute(query)
        print(results.fetchall())



# Insert the get_dataframe() function definition below - do this only when instructed in the notebook

def get_dataframe(sql_query):
    ''' 
    Connect to the PostgreSQL database server, 
    run query and return data as a pandas dataframe
    '''
    config = get_sql_config()
    # create a connection engine to the PostgreSQL server
    engine = sqlalchemy.create_engine('postgresql://user:pass@host/database',
                        connect_args=config # use dictionary with config details
                        )
    # open a conn session using 'with', execute the query, and return the results
    return pd.read_sql_query(sql=sql_query, con=engine)

# Insert the get_engine() function definition below - when instructed

def get_engine():
    sql_config = get_sql_config()
    engine = sqlalchemy.create_engine('postgresql://user:pass@host/database',
                        connect_args=sql_config
                        )
    return engine

# def build_table(engine, table_name, dataframe):
#     if engine!=None:
#         try:
#             dataframe.to_sql(name=table_name, # Name of SQL table
#                             con=engine, # Engine or connection
#                             if_exists='replace', # Drop the table before inserting new values 
#                             schema=schema, # Use schmea that was defined earlier
#                             index=False, # Write DataFrame index as a column
#                             chunksize=5000, # Specify the number of rows in each batch to be written at a time
#                             method='multi') # Pass multiple values in a single INSERT clause
#             print(f"The {table_name} table was imported successfully.")
#     # Error handling
#         except (Exception, psycopg2.DatabaseError) as error:
#             print(error)
#             engine = None

def build_main_df():
    pass

def build_name_df():
    pass



def build_dataframe_from_XML(xtree):
    main_d = [] 
    name_d = []
    nump_comm_d = []
    age_comm_d = []
    lang_d_comm = []
    b_cat = []
    b_mech = []
    b_family = []
    b_subdomain = []
    b_expansion = []
    b_honor = []
    b_designer = []
    b_artist = []
    b_publisher = []
    b_statistics = []
    b_marketplace = []
    b_podcast = []
    b_implementation = []
    b_videogames = []

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
        for node2 in node.findall('name'):
            name_d.append({"id": id ,"name": node2.text})
        for node2 in node.findall('boardgamecategory'):
            b_cat.append({"id": id ,"cat_id": node2.attrib['objectid'] ,"cat_name": node2.text})
        for node2 in node.findall('boardgamecategory'):
            b_subdomain.append({"id": id ,"cat_id": node2.attrib['objectid'] ,"cat_name": node2.text})
        for node2 in node.findall('boardgamemechanic'):
            b_mech.append({"id": id ,"cat_id": node2.attrib['objectid'] ,"cat_name": node2.text})
        for node2 in node.findall('boardgamefamily'):
            b_family.append({"id": id ,"cat_id": node2.attrib['objectid'] ,"cat_name": node2.text})
        for node2 in node.findall('boardgameexpansion'):
            b_expansion.append({"id": id ,"cat_id": node2.attrib['objectid'] ,"cat_name": node2.text})
        for node2 in node.findall('boardgamehonor'):
            b_honor.append({"id": id ,"cat_id": node2.attrib['objectid'] ,"cat_name": node2.text})
        for node2 in node.findall('boardgamedesigner'):
            b_designer.append({"id": id ,"cat_id": node2.attrib['objectid'] ,"cat_name": node2.text})
        for node2 in node.findall('boardgameartist'):
            b_artist.append({"id": id ,"cat_id": node2.attrib['objectid'] ,"cat_name": node2.text})
        for node2 in node.findall('boardgamepublisher'):
            b_publisher.append({"id": id ,"cat_id": node2.attrib['objectid'] ,"cat_name": node2.text})
        for node2 in node.findall('boardgamepodcastepisode'):
            b_podcast.append({"id": id ,"cat_id": node2.attrib['objectid'] ,"cat_name": node2.text})
        for node2 in node.findall('boardgameimplementation'):
            b_implementation.append({"id": id ,"cat_id": node2.attrib['objectid'] ,"cat_name": node2.text})
        for node2 in node.findall('videogamebg'):
            b_videogames.append({"id": id ,"cat_id": node2.attrib['objectid'] ,"cat_name": node2.text})
        for node3 in node.findall('poll'):
            if node3.attrib['name'] == "suggested_numplayers":
                for node4 in node3:
                    for node5 in node4:
                        if node5.attrib['numvotes'] != "0":
                            nump_comm_d.append({"id": id ,"num_players_recomm": node5.attrib['value'] + " for " + node4.attrib["numplayers"] + " player(s)", "num_votes": node5.attrib['numvotes']})
            if node3.attrib['name'] == 'suggested_playerage':
                for node4 in node3:
                    for node5 in node4:
                        if node5.attrib['numvotes'] != "0":
                            age_comm_d.append({"id": id ,"age": node5.attrib['value'], "num_votes": node5.attrib['numvotes']})
            if node3.attrib['name'] == 'language_dependence':
                for node4 in node3:
                    for node5 in node4:
                        if node5.attrib['numvotes'] != "0":
                            lang_d_comm.append({"id": id ,"language_dep": node5.attrib['value'], "num_votes": node5.attrib['numvotes']})
        for node2 in node.findall('statistics'):
            for node3 in node2:
                    b_statistics.append({"id": id, 
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
        for node2 in node.findall('marketplacelistings'):
            for node3 in node2:
                    b_marketplace.append({
                    "id": id, 
                    "listdate": node3.find("listdate").text,
                    "price": node3.find("price").text,
                    "currency": node3.find("price").get("currency"),
                    "condition": node3.find("condition").text
                    })
        
        main_d.append({"id": id ,"description": description, "yearpublished": yearpublished, 
                        "min_players": minplayers,"max_players": maxplayers, "playtime":playingtime, "min_playtime":minplayingtime, 
                        "max_playtime":maxplayingtime, "min_age": min_age})
            

    df_main = pd.DataFrame(main_d).set_index("id"),
    df_name = pd.DataFrame(name_d).set_index("id"),
    df_nump_comm = pd.DataFrame(nump_comm_d).set_index("id"),
    df_age_comm = pd.DataFrame(age_comm_d).set_index("id"),
    df_lang_d_comm = pd.DataFrame(lang_d_comm).set_index("id"),
    df_b_cat = pd.DataFrame(b_cat).set_index("id"),
    df_b_mech = pd.DataFrame(b_mech).set_index("id"),
    b_family = pd.DataFrame(b_family).set_index("id"),
    b_expansion = pd.DataFrame(b_expansion).set_index("id"),
    b_honor = pd.DataFrame(b_honor).set_index("id"),
    b_designer = pd.DataFrame(b_designer).set_index("id"),
    b_artist = pd.DataFrame(b_artist).set_index("id"),
    b_publisher = pd.DataFrame(b_publisher).set_index("id"),
    b_statistics = pd.DataFrame(b_statistics).set_index("id"),
    b_marketplace = pd.DataFrame(b_marketplace).set_index("id"),
    b_subdomain = pd.DataFrame(b_subdomain).set_index("id"),
    b_podcast =pd.DataFrame(b_podcast).set_index("id"),
    b_implementation =pd.DataFrame(b_implementation).set_index("id"),
    b_videogames =pd.DataFrame(b_videogames).set_index("id")
    