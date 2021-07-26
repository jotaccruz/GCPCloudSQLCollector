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
                #sqlinstance['state'] = instances['state']
                #sqlinstance['databaseVersion'] = instances['databaseVersion']
                #sqlinstance['region'] = instances['region']
                #sqlinstance['gceZone'] = instances['gceZone']
                ##sqlinstance['SELFLINK'] = instances['selfLink']
                #sqlinstance['CONNECTION'] = instances['connectionName']
                #sqlinstance['AVAILABILITY'] = instances['settings']['availabilityType']
                #sqlinstance['BACKUP'] = instances['settings']['backupConfiguration']['enabled']
                #sqlinstance['BRETENTION'] = instances['settings']['backupConfiguration']['backupRetentionSettings']['retainedBackups']
                #sqlinstance['RECOVERY'] = instances['settings']['backupConfiguration']['binaryLogEnabled']
                #sqlinstance['LRETENTION'] = instances['settings']['backupConfiguration']['transactionLogRetentionDays']
                #for ips in instances['ipAddresses']:
                #    if ips['type']=='PRIMARY':
                #        sqlinstance['PRIMARY'] = ips['ipAddress']
                #    if ips['type']=='PRIVATE':
                #        sqlinstance['PRIVATE'] = ips['ipAddress']
            sqlinstances.append(sqlinstance)
    #https://cloud.google.com/sql/docs/sqlserver/import-export/importing
    #add_bucket_iam_member("dba-freenas","roles/storage.admin","serviceAccount:" + EmailAddress)
    return sqlinstances
# [END list_sql_instances]


# [START list_sql_instance_databases]
def list_sql_instance_databases(cloudsql,projectName,instanceName):
    sqlDatabases = []
    try:
        req = cloudsql.databases().list(project=projectName,instance=instanceName)
        resp = req.execute()
        #print (resp)

        for databases in resp['items']:
            if databases['name'] not in ['sys','mysql','information_schema','performance_schema']:
                sqlDatabase = {}
                sqlDatabase['INSTANCE'] = databases['instance']
                sqlDatabase['DATABASE'] = databases['name']
                sqlDatabases.append(sqlDatabase)

    except Exception as error:
        return sqlDatabases
    return sqlDatabases
# [END list_sql_instance_databases]

# [START list_sql_instance_users]
def list_sql_instance_users(cloudsql,projectName,instanceName):
    sqlUsers = []
    try:
        req = cloudsql.users().list(project=projectName,instance=instanceName)
        resp = req.execute()

        if 'error' not in resp:
            for users in resp['items']:
                sqlUser = {}
                sqlUser['INSTANCE'] = users['instance']
                sqlUser['USERNAME'] = users['name']
                sqlUser['HOST'] = users['host']
                #sqlUser['DISABLED'] = users['sqlserverUserDetails']['disabled']
                #sqlUser['ROLES'] = users['sqlserverUserDetails']['serverRoles']

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
