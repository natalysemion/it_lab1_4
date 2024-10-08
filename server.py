import grpc
from concurrent import futures
import database_pb2
import database_pb2_grpc


class DatabaseService(database_pb2_grpc.DatabaseServiceServicer):
    def __init__(self):
        self.database = {}

    def CreateTable(self, request, context):
        if request.table_name in self.database:
            return database_pb2.CreateTableResponse(message="Table already exists.")

        self.database[request.table_name] = {'fields': request.fields, 'rows': []}
        return database_pb2.CreateTableResponse(message="Table created successfully.")

    def CreateRow(self, request, context):
        if request.table_name not in self.database:
            return database_pb2.CreateRowResponse(message="Table does not exist.")

        table = self.database[request.table_name]
        if len(request.values) != len(table['fields']):
            return database_pb2.CreateRowResponse(message="Invalid number of values.")

        row_id = len(table['rows'])
        table['rows'].append({'id': row_id, 'values': request.values})
        return database_pb2.CreateRowResponse(message="Row created successfully.")

    def GetAllRows(self, request, context):
        if request.table_name not in self.database:
            return database_pb2.GetAllRowsResponse(rows=[])

        rows = self.database[request.table_name]['rows']
        return database_pb2.GetAllRowsResponse(
            rows=[database_pb2.Row(id=row['id'], values=row['values']) for row in rows])

    def TableDifference(self, request, context):
        if request.table1_name not in self.database or request.table2_name not in self.database:
            return database_pb2.TableDifferenceResponse(difference=[])

        table1 = self.database[request.table1_name]['rows']
        table2 = self.database[request.table2_name]['rows']

        # Збираємо всі рядки з обох таблиць у множини для порівняння
        set_table1 = {tuple(value.value for value in row['values']) for row in table1}
        set_table2 = {tuple(value.value for value in row['values']) for row in table2}

        # Різниця - це рядки, які є в table1, але не в table2
        difference = set_table1 - set_table2

        # Формуємо відповіді
        rows = []
        for row in difference:
            values = [database_pb2.Value(field_name="id", value=str(row[0])),
                      database_pb2.Value(field_name="name", value=row[1])]
            rows.append(database_pb2.Row(id=len(rows), values=values))

        return database_pb2.TableDifferenceResponse(difference=rows)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    database_pb2_grpc.add_DatabaseServiceServicer_to_server(DatabaseService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
