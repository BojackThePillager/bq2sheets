from google.cloud import bigquery
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set up authentication using a service account key file
service_account_key = '/path/to/service-account-key.json'
project_id = 'your-project-id'

# Initialize the BigQuery client
client = bigquery.Client.from_service_account_json(service_account_key)

# Define the BigQuery dataset and table you want to query
dataset_id = 'your-dataset-id'
table_id = 'your-table-id'

# Define the Google Sheet credentials and ID
credentials = ServiceAccountCredentials.from_json_keyfile_name(service_account_key, scopes=['https://spreadsheets.google.com/feeds'])
sheet_id = 'your-sheet-id'

# Define the Google Sheet worksheet name
worksheet_name = 'Sheet1'

# Define the SQL query to retrieve the data from the table
sql_query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_id}`"

# Execute the query
query_job = client.query(sql_query)

# Fetch the query results
results = query_job.result()

# Initialize the Google Sheet client
gc = gspread.authorize(credentials)

# Open the Google Sheet by ID
sheet = gc.open_by_key(sheet_id)

# Select the worksheet by name
worksheet = sheet.worksheet(worksheet_name)

# Clear existing data in the worksheet
worksheet.clear()

# Write the results to the Google Sheet
cell_list = worksheet.range(1, 1, results.total_rows, results.total_columns)
cell_values = list(results)
for cell in cell_list:
    cell.value = cell_values[cell.row-1][cell.col-1]
worksheet.update_cells(cell_list)
