# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


#Service Account: mssql-restore-test@ti-is-devenv-01.iam.gserviceaccount.com
#SET GOOGLE_APPLICATION_CREDENTIALS=C:\PHome\GCPSQLAutoIn\21a77830d937.json

import argparse
from googleapiclient.discovery import build
from google.auth import compute_engine
import pandas as pd
import modules
from modules import *
#import credential
#from credential import *

import datetime
import logging
import os
import sys

from flask import Flask, render_template, request, Response

app = Flask(__name__)

logger = logging.getLogger()
project = ""
instances = []

#@app.before_first_request
#def create_tables():
#    global db
#    db = db or init_connection_engine()
#    # Create tables (if they don't already exist)
#    with db.connect() as conn:
#        conn.execute(
#            "CREATE TABLE IF NOT EXISTS metacloudsql "
#            "( entity VARCHAR(150) NOT NULL, columndict JSON NOT NULL, PRIMARY KEY (entity) );"
#        )


def menu():
    global project
    global instances

    #menu()
    options = {
    "1":("Projects",cloudsqlprojects),
    "2":("CloudSQL",cloudsql),
    "3":("Databases",cloudsqldatabases),
    "4":("Users",cloudsqlusers),
    "5":("All",cloudsqlusers),
    "6":("Quit",my_quit_fn)
    }

    print("")

    for key in sorted(options.keys()):
        print (" " + key+":" + options[key][0])

    print("\n")
    ans = input("Make A Choice: ")
    options.get(ans,[None,invalid])[1]()

    menu()

def cloudsql():
    global project
    global instances
    # Construct the service object for the interacting with the Cloud SQL Admin API.
    cloudsql = build('sqladmin','v1beta4')
    instances = list_sql_instances(cloudsql, project)

    #for dict in instances:
    #    flat = flatten_json(dict)
    #    print(pd.json_normalize(flat))

    #print(pd.json_normalize(instances,'FLAGS',['NAME','PUBLIC','PRIVATE','VERSION','ZONE','BACKUPS','RETENTION']))

    cs = pd.DataFrame(instances)
    if not cs.empty:
        print("\n")
        print('CloudSQL Instances in project %s:' % (project))
        print("\n")
        print(cs.sort_values(by=['NAME'], ascending=False).reset_index(drop=True))
        print("\n")

    return instances

def cloudsqldatabases():
    global project
    global instances

    # Construct the service object for the interacting with the Cloud SQL Admin API.
    cloudsql = build('sqladmin','v1beta4')

    databases = []
    for instance in instances:
        databases = databases + list_sql_instance_databases(cloudsql,project,instance['NAME'])

    dbs = pd.DataFrame(databases)
    if not dbs.empty:
        print("\n")
        print('Databases in project %s by Instance:' % (project))
        print("\n")
        print(dbs.sort_values(by=['INSTANCE'], ascending=False).reset_index(drop=True))
        print("\n")
    return databases

def cloudsqlusers():
    global project
    global instances
    # Construct the service object for the interacting with the Cloud SQL Admin API.
    cloudsql = build('sqladmin','v1beta4')

    users = []
    for instance in instances:
        users = users + list_sql_instance_users(cloudsql,project,instance['NAME'])

    df = pd.DataFrame(users)

    print("\n")
    print('Users in project %s by Instance:' % (project))
    print("\n")
    print(df.sort_values(by=['INSTANCE'], ascending=False).reset_index(drop=True))
    print("\n")

    return users

def cloudsqlprojects():
    # Construct the service object for the interacting with the Cloud SQL Admin API.
    computer = build('cloudresourcemanager', 'v1')
    print("\n")
    projects = list_projects(computer)

    df = pd.DataFrame(projects)
    toprint = df.sort_values(by=['NAME'], ascending=False).reset_index(drop=True)

    print("GCP Projects: \n")
    print(toprint)
    print("\n")

    choice=input("Please choose a project name: ")

    return(choice)

def my_quit_fn():
   raise SystemExit

def invalid():
   print ("INVALID CHOICE!")

# [START run]
def main(proj, wait=True):

    global project
    project = proj

    #credential = mycredential()

    menu()

    #sqlexec0 = readFileFromOS(getFileUrl("databases.sql","queries"))

    #for row in db_Query(sqlexec0,'','ISJCruz',mysqlpsw):
    #    do something
    #if wait:
    #    input()

    #print('Listing Databases in each instance.')

    #print("""
#Database imported.
#Once the Database is imported press enter to DELETE the instance.
#""".format(project))

#    if wait:
#        input()

#    print('Deleting CloudSQL instance.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('project_id', help='Your Google Cloud project ID.')

    args = parser.parse_args()

    main(args.project_id)
# [END run]
#python main.py ti-is-devenv-01
