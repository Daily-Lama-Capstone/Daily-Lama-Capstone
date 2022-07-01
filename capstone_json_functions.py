import pandas as pd

keys_to_keep = ["name",
            "blurb",
            "goal",
            "pledged",
            "state",
            #"slug",
            #"disable_communication",
            "country",
            "country_displayable_name",
            "currency",
            #"currency_trailing_code",
            "deadline",
            "state_changed_at",
            "created_at",
            "launched_at",
            "backers_count",
            "static_usd_rate",
            "usd_pledged",
            "converted_pledged_amount",
            "fx_rate",
            "usd_exchange_rate",
            "current_currency",
            "usd_type",
            "creator",
            "location",
            "category",
            #"profile",
            #"spotlight",
            # "urls",
            "rewards"]


def create_json_df(filepath):
    json_df = pd.read_json(filepath, lines=True)
    json_df.drop(["table_id", "robot_id", "run_id"], axis=1, inplace=True)
    return json_df


def df_from_json(json_df):
    keys_to_pop = keys_for_trash(json_df)
    df = pd.DataFrame()
    for idx, row in json_df.iterrows():
        #keys_to_pop = []
        this_row = dict(row["data"])
        # for key in this_row.keys():
        #     if key not in keys_to_keep:
        #         keys_to_pop.append(key)
        for trash_keys in keys_to_pop:
            this_row.pop(trash_keys)
        if dict(this_row["category"])["id"] == 34:
            df_temp = pd.json_normalize(this_row, sep='_')
            df = pd.concat([df, df_temp])
    return df





def keys_for_trash(df):
    for idx,row in df.iterrows():
        keys_to_pop = []
        this_row = dict(row["data"])
        for key in this_row.keys():
            if key not in keys_to_keep:
                keys_to_pop.append(key)
        break
    return keys_to_pop