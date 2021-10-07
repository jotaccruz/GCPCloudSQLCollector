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

# Import the necessary packages
from consolemenu import *
from consolemenu.items import *
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
projects = []
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


def show_menu():
    print ("\nMenu")
    print ("-----------------")
    print ("[1] Projects")
    print ("[2] CloudSQLs")
    print ("[3] Databases")
    print ("[4] Users")
    print ("[5] Export")
    print ("[Q] Exit\n")

def menu(proj):
    while True:
        show_menu()
        choice = input('Enter your choice: ').lower()
        if choice == '1':
            cloudsqlprojects()
        elif choice == '2':
            instances=cloudsqlinstances(proj)
        elif choice == '3':
            cloudsqldatabases(proj,instances)
        elif choice == '4':
            cloudsqlusers(proj,instances)
        elif choice == 'q':
            return
        else:
            print(f'Not a correct choice: <{choice}>, try again')

def cloudsqlprojects():
    # Construct the service object for the interacting with the Cloud SQL Admin API.
    computer = build('cloudresourcemanager', 'v1')
    print("\n")
    projects = list_projects(computer)

    dp = pd.DataFrame(projects)
    toprint = dp.sort_values(by=['NAME'], ascending=False).reset_index(drop=True)

    print("GCP Projects: \n")
    print(toprint)
    print("\n")
    input("Press Enter to continue...")


    return projects

def cloudsqlinstances(proj):
    # Construct the service object for the interacting with the Cloud SQL Admin API.
    cloudsql = build('sqladmin','v1beta4')
    if not proj:
        computer = build('cloudresourcemanager', 'v1')
        projects = list_projects(computer)
        for project in projects:
            instances = list_sql_instances(cloudsql, project["NAME"])
    else:
        instances = list_sql_instances(cloudsql, proj)

    cs = pd.DataFrame(instances)
    if not cs.empty:
        print("\n")
        print('CloudSQL Instances')#s in project %s:' % (project))
        print("\n")
        print(cs)
        print("\n")

    return instances

def cloudsqldatabases(proj,intances):

    # Construct the service object for the interacting with the Cloud SQL Admin API.
    cloudsql = build('sqladmin','v1beta4')

    databases = []
    if not proj:
        computer = build('cloudresourcemanager', 'v1')
        projects = list_projects(computer)
        for project in projects:
            instances = list_sql_instances(cloudsql, project["NAME"])

    if instances:
        for instance in instances:
            databases = list_sql_instance_databases(cloudsql,proj,instance['NAME'])
    else:
        databases=["Empty"]

    dbs = pd.DataFrame(databases)
    if not dbs.empty:
        print("\n")
        print('Databases in project %s by Instance:' % (project))
        print("\n")
        print(dbs)
        print("\n")

    return databases

def cloudsqlusers(proj):

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


    # [START run]
def main(proj):

    # Finally, we call show to show the menu and allow the user to interact
    menu(proj)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--p', help='Your Google Cloud project ID.')

    args = parser.parse_args()

    main(args.p)
    #main()
# [END run]


def my_quit_fn():
   raise SystemExit

def invalid():
   print ("INVALID CHOICE!")

#python main.py ti-is-devenv-01
