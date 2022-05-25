# CloudSQL Collector
GCP CloudSQL Database Collector

<b>Runtime:</b> Python 3.9 <br>
<b>Entry point:</b> CloudSQLCollector

<b>Runtime service account</b><br>
Assign a service account with the following permissions:


<b>Runtime environment variables</b>

<table>
<thead>
  <tr>
    <th>NAME</th>
    <th>VALUE Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>CLOUD_SQL_CONNECTION_NAME</td>
    <td>Cloud MySQL name where mandatory auto config database will live</td>
  </tr>
  <tr>
    <td>DB_USER</td>
    <td>Cloud Function Service account name (dba-automate<strike>@domain.com</strike>)</td>
  </tr>
  <tr>
    <td>DB_NAME</td>
    <td>Auto config database name</td>
  </tr>
  <tr>
    <td>BUCKET</td>
    <td>Bucket name where files will be saved</td>
  </tr>
  <tr>
    <td>URL</td>
    <td>The directory inside the bucket where generated files will be saved (inventory/)</td>
  </tr>
</tbody>
</table><br>

<b>Connections Settings</b><br><br>
<b>Ingress Settings:</b><br>
Allow Internal Traffic Only<br><br>
<b>Egress Settings:</b><br>
VPC Connector<br>
Route all traffic through the VPC connector<br>
