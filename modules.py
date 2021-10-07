from pprint import pprint
from googleapiclient.errors import HttpError
import dbDriver
from dbDriver import *
import json
from glom import glom
from glom import SKIP
import credential
from credential import *

# This global variable is declared with a value of `None`, instead of calling
# `init_connection_engine()` immediately, to simplify testing. In general, it
# is safe to initialize your database connection pool when your script starts
# -- there is no need to wait for the first request.
db = None
# [START list_projects]
# Permissions required: resourcemanager.projects.get
def list_projects(compute):
    request = compute.projects().list()
    response = request.execute()
    projects = []

    #print (response)
    for project in response.get('projects', []):
        # TODO: Change code below to process each `project` resource:
        proj = {}
        proj['NAME'] = project['name']

        projects.append(proj)
    return projects
# [END list_projects]

def get_entity_fields(pentity):
    global db
    mycredentials = mycredential()
    db = db or init_connection_engine(mycredentials.token)

    fields = []
    with db.connect() as conn:
        stmt = sqlalchemy.text(
            "SELECT entity, keyaddress, keyname, keyalias FROM metadataapi WHERE entity=:entity AND status=1 ORDER BY orderlist ASC"
        )
        # Execute the query and fetch all results
        entity_fields = conn.execute(stmt,entity=pentity).fetchall()
        # Convert the results into a list of dicts representing votes
        for row in entity_fields:
            fields.append(row)
    return fields

# [START list_sql_instances]
def list_sql_instances(cloudsql,projectname):
    req = cloudsql.instances().list(project=projectname)
    resp = req.execute()
    #print(glom(resp['items'][1],'name'))

    if 'error' not in resp:
        sqlinstances = []
        cloudsql_fields = get_entity_fields("cloudsql")
        for instances in resp['items']:
            sqlinstance = {}
            #print(instances)
            for key in cloudsql_fields:
                sqlinstance[key[3]] = glom(instances,key[1],default='N/A')
            sqlinstances.append(sqlinstance)
    return sqlinstances
# [END list_sql_instances]


# [START list_sql_instance_databases]
def list_sql_instance_databases(cloudsql,projectName='na',instanceName='na'):
    sqlDatabases = []
    try:
        if instanceName=='na':
            req = cloudsql.databases().list(project=projectName)
        else:
            req = cloudsql.databases().list(project=projectName,instance=instanceName)

        resp = req.execute()

        if 'error' not in resp:
            databases_fields = get_entity_fields("cloudsql_databases")
            for databases in resp['items']:
                sqlDatabase = {}
                #if databases['name'] not in ['sys','mysql','information_schema','performance_schema']:
                #print(instances)
                for key in databases_fields:
                    sqlDatabase[key[3]] = glom(databases,key[1],default='N/A')
                sqlDatabases.append(sqlDatabase)
    except Exception as error:
        sqlDatabases="Error"
        return sqlDatabases
    return sqlDatabases
# [END list_sql_instance_databases]

# [START list_sql_instance_users]
def list_sql_instance_users(cloudsql,projectName,instanceName):
    try:
        req = cloudsql.users().list(project=projectName,instance=instanceName)
        resp = req.execute()

        if 'error' not in resp:
            sqlUsers = []
            users_fields = get_entity_fields("cloudsql_users")
            for users in resp['items']:
                sqlUser = {}
                #if databases['name'] not in ['sys','mysql','information_schema','performance_schema']:
                #print(instances)
                for key in users_fields:
                    sqlUser[key[3]] = glom(users,key[1],default='N/A')
                sqlUsers.append(sqlUser)
    except HttpError as err:
        return sqlUsers
    return sqlUsers
# [END list_sql_instance_users]

# [START getFileUrl]
def getFileUrl(filename,directory):
        if getattr(sys, 'frozen', False): # Running as compiled
            running_dir = sys._MEIPASS + "/" + directory + "/" #"/files/" # Same path name than pyinstaller option
        else:
            running_dir = "./" + directory + "/" # Path name when run with Python interpreter
        FileName = running_dir + filename #"moldmydb.png"
        return FileName
# [END getFileUrl]

# [START readFileFromOS]
def readFileFromOS(filename):
    with open(filename,'r') as file:
        data=file.read()
    return data
# [END readFileFromOS]


# [START wait_for_operation]
def wait_for_operation(cloudsql, project, operation):
    print('Waiting for operation to finish...')
    while True:
        result = cloudsql.operations().get(
            project=project,
            operation=operation).execute()

        if result['status'] == 'DONE':
            print("done.")
            if 'error' in result:
                raise Exception(result['error'])
            return result
        time.sleep(1)
# [END wait_for_operation]
# wait_for_operation(cloudsql, "ti-is-devenv-01", operation)

def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out
