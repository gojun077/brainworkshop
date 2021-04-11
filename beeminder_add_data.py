#!/usr/bin/env python3
# beeminder_add_data.py
# Created on: Apr 12 2021
# Created by: gojun077@gmail.com
# Last Updated: Apr 12 2021
# Contributors: gojun077@gmail.com
#
# A helper script to increment a beeminder goal by + 1.0 via the Beeminder
# API when a dual N-back session in brainworkshop is completed. The
# Beeminder username, goalname, auth_token, and comment string will be read
# from a json file named "beeminder.json" located in the same dir as this
# script.


import datetime
import json
import requests


def submit():
    """
    Increment Beeminder goal by + 1.0
    """
    try:
        with open("beeminder.json","r") as f:
            bmndrD = json.load(f)
            url = "https://www.beeminder.com/api/v1/users"
            epoch_utc = int(datetime.datetime.utcnow().timestamp())
            myuser, mygoal = bmndrD["username"], bmndrD["goalname"]
            endpt = f"{url}/{myuser}/goals/{mygoal}/datapoints.json"
            payload = {"auth_token": bmndrD["auth_token"],
                       "timestamp": epoch_utc,
                       "value": 1.0,
                       "comment": bmndrD["comment"]}
            header = {"Content-Type": "application/json"}
            resp_post = requests.post(endpt, headers=header,
                                      data=json.dumps(payload))
            if resp_post.status_code != 200:
                print(f"HTTP Status: {resp_post.status_code}")
                print(f"Error msg: {resp_post.text}")
                raise Exception
            else:
                print("Data successfully submitted to Beeminder")
                resp_data = resp_post.json()
                print(resp_data)
    except (IOError, ValueError, EOFError) as e:
        print(e)
    except:
        print("error occurred while trying to send data to Beeminder...")


def main():
    submit()


if __name__ == "__main__":
    main()
