from pprint import pprint

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



# [START list_sql_instances]
def list_sql_instances(cloudsql,projectname):
    req = cloudsql.instances().list(project=projectname)
    resp = req.execute()

    if 'error' not in resp:
        sqlinstances = []

        for instances in resp['items']:
            sqlinstance = {}
            sqlinstance['NAME'] = instances['name']
            sqlinstance['STATUS'] = instances['state']
            sqlinstance['DATABASE_VERSION'] = instances['databaseVersion']
            sqlinstance['LOCATION'] = instances['region']
            for ips in instances['ipAddresses']:
                if ips['type']=='PRIMARY':
                    sqlinstance['PRIMARY_ADDRESS'] = ips['ipAddress']
                if ips['type']=='PRIVATE':
                    sqlinstance['PRIVATE_ADDRESS'] = ips['ipAddress']
            sqlinstances.append(sqlinstance)
    #https://cloud.google.com/sql/docs/sqlserver/import-export/importing
    #add_bucket_iam_member("dba-freenas","roles/storage.admin","serviceAccount:" + EmailAddress)
    return sqlinstances
# [END list_sql_instances]


# [START list_sql_instance_databases]
def list_sql_instance_databases(cloudsql,projectName,instanceName):
    req = cloudsql.databases().list(project=projectName,instance=instanceName)
    resp = req.execute()
    print (resp)
    sqlDatabases = []

    if 'error' not in resp:
        for databases in resp['items']:
            sqlDatabase = {}

            sqlDatabase['INSTANCE'] = databases['instance']
            sqlDatabase['NAME'] = databases['name']

            sqlDatabases.append(sqlDatabase)
    return sqlDatabases
# [END list_sql_instance_databases]

# [START list_sql_instance_users]
def list_sql_instance_users(cloudsql,projectName,instanceName):
    req = cloudsql.users().list(project=projectName,instance=instanceName)
    resp = req.execute()
    sqlUsers = []

    for users in resp['items']:
        sqlUser = {}

        sqlUser['INSTANCE'] = users['instance']
        sqlUser['NAME'] = users['name']
        sqlUser['HOST'] = users['host']
        #sqlUser['DISABLED'] = users['sqlserverUserDetails']['disabled']
        #sqlUser['ROLES'] = users['sqlserverUserDetails']['serverRoles']

        sqlUsers.append(sqlUser)
    return sqlUsers
# [END list_sql_instance_users]


# [START list_sql_instance_users]
def list_sql_instance_users(cloudsql,projectName,instanceName):
    req = cloudsql.users().list(project=projectName,instance=instanceName)
    resp = req.execute()
    sqlUsers = []

    for users in resp['items']:
        sqlUser = {}

        sqlUser['INSTANCE'] = users['instance']
        sqlUser['NAME'] = users['name']
        sqlUser['HOST'] = users['host']
        #sqlUser['DISABLED'] = users['sqlserverUserDetails']['disabled']
        #sqlUser['ROLES'] = users['sqlserverUserDetails']['serverRoles']

        sqlUsers.append(sqlUser)
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
