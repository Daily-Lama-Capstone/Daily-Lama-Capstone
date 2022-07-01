import pandas as pd


def df_from_json(filepath,keys_to_keep):
    json_df = pd.read_json(filepath,lines=True)
    json_df.drop(["table_id","robot_id", "run_id"],axis=1,inplace=True)
    df = pd.DataFrame()
    for idx,row in json_df.iterrows():
        keys_to_pop = []
        this_row = dict(row["data"])
        for key in this_row.keys():
            if key not in keys_to_keep:
                keys_to_pop.append(key)
        for trash_keys in keys_to_pop:
            this_row.pop(trash_keys)
        if dict(this_row["category"])["id"] == 34:
            df_temp = pd.json_normalize(this_row,sep='_')
            df = pd.concat([df,df_temp])
    return df
    
