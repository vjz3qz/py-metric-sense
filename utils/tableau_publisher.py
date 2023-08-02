import tableauserverclient as tsc


class TableauPublisher:
    def __init__(self, file_path, project_id, data_source_name):
        self.file_path = file_path
        self.project_id = project_id
        self.data_source_name = data_source_name

    def publish_to_tableau_server(self):
        try:
            tableau_auth = tsc.TableauAuth('USERNAME', 'PASSWORD', 'SITE_ID')
            server = tsc.Server('http://SERVER_URL')

            with server.auth.sign_in(tableau_auth):
                new_datasource = tsc.DatasourceItem(self.project_id, name=self.data_source_name)
                new_datasource = server.datasources.publish(new_datasource, self.file_path, 'Overwrite')
                print(f'Successfully published datasource {self.data_source_name} to Tableau Server.')
        except Exception as e:
            print(f"Error: An unexpected error occurred while publishing to Tableau Server. {str(e)}")
