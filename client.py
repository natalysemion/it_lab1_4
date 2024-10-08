import grpc
import database_pb2
import database_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = database_pb2_grpc.DatabaseServiceStub(channel)

        # Створення таблиці
        response = stub.CreateTable(database_pb2.CreateTableRequest(
            table_name="Users",
            fields=[
                database_pb2.Field(name="id", type="integer"),
                database_pb2.Field(name="name", type="string"),
            ]
        ))
        print(response.message)

        # Додавання рядка до першої таблиці
        response = stub.CreateRow(database_pb2.CreateRowRequest(
            table_name="Users",
            values=[
                database_pb2.Value(field_name="id", value="1"),
                database_pb2.Value(field_name="name", value="Alice"),
            ]
        ))
        print(response.message)

        # Створення другої таблиці
        response = stub.CreateTable(database_pb2.CreateTableRequest(
            table_name="Users_Archived",
            fields=[
                database_pb2.Field(name="id", type="integer"),
                database_pb2.Field(name="name", type="string"),
            ]
        ))
        print(response.message)

        # Додавання рядка до другої таблиці
        response = stub.CreateRow(database_pb2.CreateRowRequest(
            table_name="Users_Archived",
            values=[
                database_pb2.Value(field_name="id", value="1"),
                database_pb2.Value(field_name="name", value="Bob"),
            ]
        ))
        print(response.message)

        # Отримання різниці між таблицями
        response = stub.TableDifference(database_pb2.TableDifferenceRequest(
            table1_name="Users",
            table2_name="Users_Archived"
        ))

        print("Different rows in Users compared to Users_Archived:")
        for row in response.difference:
            print(f"Row ID: {row.id}, Values: {[f'{value.field_name}: {value.value}' for value in row.values]}")

if __name__ == '__main__':
    run()
