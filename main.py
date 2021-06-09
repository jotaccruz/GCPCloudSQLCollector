#Service Account: mssql-restore-test@ti-is-devenv-01.iam.gserviceaccount.com
#SET GOOGLE_APPLICATION_CREDENTIALS=C:\PHome\GCPSQLAutoIn\ti-is-devenv-01-e494bc35aeae.json
import argparse
from googleapiclient.discovery import build
import pandas as pd
import modules
from modules import *

# [START run]
def main(project, wait=True):

    computer = build('cloudresourcemanager', 'v1')
    projects = list_projects(computer)

    df = pd.DataFrame(projects)
    toprint = df.sort_values(by=['NAME'], ascending=False).reset_index(drop=True)

    print('GCP Projects %s:')
    print(toprint)

    # Construct the service object for the interacting with the Cloud SQL Admin API.
    cloudsql = build('sqladmin','v1beta4')
    instances = list_sql_instances(cloudsql, project)

    df = pd.DataFrame(instances)
    toprint = df.sort_values(by=['NAME'], ascending=False).reset_index(drop=True)


    print('CloudSQL Instances in project %s:' % (project))
    print(toprint)

    databases = []
    for instance in instances:
        databases = databases + list_sql_instance_databases(cloudsql,project,instance['NAME'])

    df = pd.DataFrame(databases)
    toprint = df.sort_values(by=['INSTANCE'], ascending=False).reset_index(drop=True)

    print('Databases in project %s by Instance:' % (project))
    print(toprint)


    users = []
    for instance in instances:
        users = users + list_sql_instance_users(cloudsql,project,instance['NAME'])

    df = pd.DataFrame(users)
    toprint = df.sort_values(by=['INSTANCE'], ascending=False).reset_index(drop=True)

    print('Users in project %s by Instance:' % (project))
    print(toprint)

    sqlexec0 = readFileFromOS(getFileUrl("databases.sql","queries"))

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
