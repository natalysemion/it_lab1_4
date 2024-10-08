const { TableDifferenceRequest } = require('./database_pb');
const { DatabaseServiceClient } = require('./database_grpc_web_pb');

const client = new DatabaseServiceClient('http://localhost:50051');

document.getElementById('createTableBtn').addEventListener('click', () => {
    const tableName = document.getElementById('tableName').value;

    const request = new CreateTableRequest();
    request.setTableName(tableName);
    request.setFields([
        { name: "id", type: "integer" },
        { name: "name", type: "string" }
    ]);

    client.createTable(request, {}, (err, response) => {
        if (err) {
            console.error(err);
        } else {
            alert(response.getMessage());
        }
    });
});

document.getElementById('createRowBtn').addEventListener('click', () => {
    const rowName = document.getElementById('rowName').value;

    const request = new CreateRowRequest();
    request.setTableName("Users");
    request.setValues([
        { field_name: "id", value: "1" },
        { field_name: "name", value: rowName }
    ]);

    client.createRow(request, {}, (err, response) => {
        if (err) {
            console.error(err);
        } else {
            alert(response.getMessage());
        }
    });
});

document.getElementById('getAllRowsBtn').addEventListener('click', () => {
    const request = new GetAllRowsRequest();
    request.setTableName("Users");

    client.getAllRows(request, {}, (err, response) => {
        const rowsContainer = document.getElementById('rowsContainer');
        rowsContainer.innerHTML = '';

        if (err) {
            console.error(err);
        } else {
            response.getRowsList().forEach(row => {
                rowsContainer.innerHTML += `<div>Row ID: ${row.getId()}, Values: ${JSON.stringify(row.getValuesList())}</div>`;
            });
        }
    });
});

document.getElementById('getTableDifferenceBtn').addEventListener('click', () => {
    const table1Name = document.getElementById('table1Name').value;
    const table2Name = document.getElementById('table2Name').value;

    const request = new TableDifferenceRequest();
    request.setTable1Name(table1Name);
    request.setTable2Name(table2Name);

    client.tableDifference(request, {}, (err, response) => {
        if (err) {
            console.error(err);
        } else {
            const differenceContainer = document.getElementById('differenceContainer');
            differenceContainer.innerHTML = '';
            response.getDifferenceList().forEach(row => {
                differenceContainer.innerHTML += `<div>Row ID: ${row.getId()}, Values: ${JSON.stringify(row.getValuesList())}</div>`;
            });
        }
    });
});
