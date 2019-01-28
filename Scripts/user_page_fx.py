from Scripts import utils

# import pandas as pd
# import json
# from pprint import pprint
#
# data_path = 'Data/data.json'
# with open(data_path, 'rb') as inp:
#     data = json.load(inp)
#
# data.keys()
# user_df = data['User']
# data1 = pd.DataFrame(data["Messages"])
# data1.head()
# data2 = data1.to_dict()
# data2.keys()
# # mets = get_userdf_parts(user_df)
# # mets['birth_date'][:10]
# # pprint(mets)

def get_userdf_parts(user_df):

    """
    Parse user profile part of json

    user_df (dict):
        Raw dictionary from json that contains user information

    Returns
    user_df_kept (dict)
        Subset of user_df with keys of interest

    Parses user file... this section contains a lot of person information which I purposely try to avoid

    """
    keep_keys = ['active_time', 'age_filter_max', 'age_filter_min', 'bio', 'birth_date',
                 'connection_count', 'create_date',  'education', 'gender', 'gender_filter',
                 'jobs', 'schools']

    for key in keep_keys:
        if key not in user_df:
            raise IndexError(key + " not in input keys: "+ str(user_df.keys()))

    user_df_kept = {k: v for k, v in user_df.items() if k in keep_keys}
    user_df_kept['birth_date'] = user_df_kept['birth_date'][:10]

    user_df_kept = utils.check_dict_types(user_df_kept)
    return(user_df_kept)



# def get_user_page_info(user_page_df):
