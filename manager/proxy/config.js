const dbconn = require("mysql");
const config = {
    pool : dbconn.createPool({
        connectionLimit : 100,
        host: 'localhost',
        port: 3306,
        user: 'tester',
        password: '123456',
        database: 'whateverdot',
        acquireTimeout: 1000000
    }),
    port : 3001,
    grpc_aggregator_port : 8084,
    grpc_collector_port : 8083,
    host: 'localhost',
};
module.exports = config;
