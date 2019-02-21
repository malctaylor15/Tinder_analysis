import json
import os
import sys
from zipfile import ZipFile
import uuid
import boto3


top_level_keys = {'Messages', 'Photos', 'Places', 'Purchases', 'Spotify', 'Usage', 'User'}
controlled_schema = {'Places': {'recentPlaces', 'blockedPlaces', 'analytics'},
'Purchases': {'subscription', 'consumable', 'boost_tracking', 'super_like_tracking'},
'Spotify': {'spotify_connected', 'spotify_theme_track'},
'Usage': {'app_opens', 'swipes_likes', 'swipes_passes', 'matches', 'messages_sent', 'messages_received'},
'User':{'active_time', 'age_filter_max', 'age_filter_min', 'bio', 'birth_date',
                 'connection_count', 'create_date',  'education', 'gender', 'gender_filter',
                 'jobs', 'schools'}}
user_drops = ['email', 'full_name', 'travel_pos', 'ip_address', 'phone_id']
user_travel_drops = ['route', 'street_number', 'lat', 'lon']

s3_client = boto3.client('s3')


def unzip_file(file_name):
    """
    Opens zip file and returns temp file path of data json
    :param file_name:
    :return:
    """

    new_temp_path = "/tmp/zip_extracts_"+str(uuid.uuid4())
    if not os.path.isdir(new_temp_path):
        os.mkdir(new_temp_path)

    # opening the zip file in READ mode
    with ZipFile(file_name, 'r') as zip:
        zip.extractall(new_temp_path)

    data_path = new_temp_path+"/data.json"
    assert(os.path.isfile(data_path))

    return(data_path)


def schema_check(input_list, control_set):

    """
    Make sure there are no duplicate in input, and both lists have same information or raises error
    :param input_list:
    :param control_set:
    :return:
    """
    errors = []
    input_set = set(input_list)

    # No dups in input
    if len(input_set) != len(input_list): errors.append("Duplicates in input list")

    # Everything in control list should be covered
    if len(control_set.difference(input_set)) != 0: errors.append(
        "Extra in control-- " + str(control_set.difference(input_set)))

    # Everything in data should be covered
    if len(input_set.difference(control_set)) != 0: errors.append(
        "Extra in control-- " + str(input_set.difference(control_set)))

    return (errors)

def drop_keys_from_dict(keys, big_dict, errors):
    """
    Drop a list of keys from dictionary, if not returns error
    :param keys:
    :param big_dict:
    :param errors:
    :return:
    """
    for key in keys:
        if key in big_dict:
            try:
                del big_dict[key]
            except:
                errors.append("Failed to drop key: " + str(key))
                pass

    return(big_dict, errors)

def handler(event, context):

    s3_bucket = "tinder-data-prod"
    for record in event['Records']:

        raw_file_name = record['s3']['object']['key']
        local_location = '/tmp/'+raw_file_name

        s3_client.download_file(s3_bucket, raw_file_name, local_location)

        # Handle .zip files and files that don't end in json
        if local_location[-4:] == ".zip":
            local_location = unzip_file(local_location)
        elif local_location[-4:] != "json":
            raise ValueError("File does not end in json")

        # Read in file
        with open(local_location, 'rb') as hnd:
            data = json.load(hnd)

        # Check schema
        data_keys = data.keys()
        errors = {}
        errors["top level"] = schema_check(data_keys, top_level_keys)

        # Drop PII
        user2 = data['User'].copy()
        data['User'], errors = drop_keys_from_dict(user_drops, user2, errors)
        data['User']['travel_location_info'], errors = drop_keys_from_dict(user_travel_drops
                                                                           , user2['travel_location_info'], errors)

        #Create new id for file
        new_id = "_".join([data['User']['create_date'], data['User']['birth_date']])
        new_file_name = "reformatted_data_"+new_id+".json"

        # Serialize for re upload
        new_tmp_upload_pth = "/tmp/"+new_file_name
        with open(new_tmp_upload_pth, "w") as hnd:
            json.dump(data, hnd)

        # Upload to s3
        bucket_location = "reformatted_json/"+new_file_name
        s3_client.upload_file(new_tmp_upload_pth, s3_bucket, bucket_location)

    return(0)


if __name__== "__main__":
    input = sys.argv[1]
    with open(input, "rb") as inp:
        test_event = json.load(inp)
    handler(test_event, None)
    print("Completed python main fx")
