import pandas as pd
import json
import os

keys_to_keep = ["name", "goal", "pledged", "state", "slug",
                "country", "currency", 'state_changed_at',
                "deadline", "created_at", "launched_at",
                "backers_count", "usd_pledged", "current_currency",
                "creator"]

all_keys = ['id', 'photo', 'name', 'blurb', 'goal', 'pledged',
            'state', 'slug', 'disable_communication', 'country',
            'country_displayable_name', 'currency', 'currency_symbol',
            'currency_trailing_code', 'deadline', 'state_changed_at',
            'created_at', 'launched_at', 'staff_pick', 'is_starrable',
            'backers_count', 'static_usd_rate', 'usd_pledged',
            'converted_pledged_amount', 'fx_rate', 'usd_exchange_rate',
            'current_currency', 'usd_type', 'creator', 'location',
            'category', 'profile', 'spotlight', 'urls', 'source_url']

keys_to_dump = [x for x in all_keys if x not in keys_to_keep]

columns_to_keep = ['name', 'goal', 'pledged', 'state', 'slug', 'country',
                   'currency', 'deadline', 'created_at',
                   'launched_at', 'backers_count', 'usd_pledged', 
                   'creator_name', 'state_changed_at']

to_datetime_columns = ['created_at',"launched_at",'deadline','state_changed_at']

def unix_to_datetime(df,columns_to_change=to_datetime_columns):
    for col in columns_to_change:
        df[col] = pd.to_datetime(df[col],unit='s')
    return df

def list_of_lines(filepath):
    with open(filepath) as fp:
        lines = fp.readlines()
    return lines


def build_df_from_lines_list(line_list, category=34):
    df = pd.DataFrame()
    for line in line_list:
        try:
            line_dict = json.loads(line[line.index('{"id":'):-2])
            if line_dict["category"]["id"] == category:
                for key in keys_to_dump:
                    try:
                        line_dict.pop(key)
                    except:
                        continue
                df_temp = pd.json_normalize(line_dict, sep='_')
                df = pd.concat([df, df_temp])
        except:
            continue
    return df


def list_of_categories(filepath, dumpfile=False):
    # read file
    with open(filepath) as fp:
        lines = fp.readlines()
    # build dict with all the category ids and "slug" names
    category_dict = dict()
    for line in lines:
        line_dict = json.loads(line[line.index('{"id":'):-2])
        category_dict[line_dict["category"]["id"]
                      ] = line_dict["category"]["slug"]
    # build list from dict and sort it
    list_of_categories = []
    for key, value in category_dict.items():
        list_of_categories.append([key, value])
    list_of_categories.sort()
    # dump result into file
    if dumpfile:
        with open("kickstarter_categories.txt", "w") as fp:
            for item in list_of_categories:
                fp.writelines(f"id: {item[0]} ---> {item[1]}\n")
    return list_of_categories


def rename_kickstarter_files(directory):
    for filename in os.listdir(directory):
        # Construct old file name
        source = f"{directory}{filename}"
        # Adding the count to the new file name and extension
        if filename.startswith("Kickstarter"):
            destination = f"{directory}{filename[12: 22]}.json"
            # Renaming the file
            os.rename(source, destination)
            print(f"Renamed: {source} ---> {destination}")
