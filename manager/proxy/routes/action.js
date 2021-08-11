var express = require("express")
var router = express.Router();
const grpc = require("@grpc/grpc-js");
const protoLoader = require("@grpc/proto-loader");
const config = require("../config");
const cors = require("cors");
const proto_path = "./proto/WorkProtocolService.proto"
const packageDefinition = protoLoader.loadSync(
    proto_path,
    {
            keepCase: true,
            longs: String,
            enums: String,
            defaults: true,
            oneofs: true
    });


const protoDescriptor = grpc.loadPackageDefinition(packageDefinition);
const kkennibGrpc = protoDescriptor.com.kkennib.grpc;
const grpc_aggregator_stub = new kkennibGrpc.WorkProtocolService(`localhost:${config.grpc_aggregator_port}`, grpc.credentials.createInsecure());
const grpc_collector_stub = new kkennibGrpc.WorkProtocolService(`localhost:${config.grpc_collector_port}`, grpc.credentials.createInsecure());

const isErr = function (err) {
    if (err !== null) {
        console.log(err);
        return true
    }
    return false
}

const existReponsedResult = function (res) {
    if (res !== undefined) {
        console.log(res);
        return true
    }
    return false
}

function strNull(v) {
    if(v===undefined || v==='undefined') return '';
    return v;
}

const log = {
    queryCallRequest: function (sql, addr) {
        console.log('===> [Begin]   SQL//Addr: ' + addr);
        console.log('===>  ↓↓↓↓↓    Request Query');
        console.log(sql);
        console.log('-------------------------------------------\n\n');
    },
    queryCallResponse: function (result, sql, addr) {
        console.log('===> [End]    SQL//Addr: ' + addr);
        console.log('===> ↓↓↓↓↓    Request Query');
        console.log(sql);
        console.log('*********  Response Data');
        console.log(result);
        console.log('-------------------------------------------\n\n');
    },
    actionCallRequest: function (data, addr) {
        console.log('===> [Begin]   POST//Addr: ' + addr);
        console.log('===>  ↓↓↓↓↓    Request Data');
        console.log(data);
        console.log('-------------------------------------------\n\n');
    },
    actionCallResponse: function (result, data, addr) {
        console.log('===> [End]    POST//Addr: ' + addr);
        console.log('===> ↓↓↓↓↓    Request Data');
        console.log(data);
        console.log('*********  Response Data');
        console.log('-------------------------------------------\n\n');
    }
};

function query(sql, addr, action) {
    log.queryCallRequest(sql, addr);
    config.pool.getConnection(function(err, conn) {
        if (err) {
            console.log('######### Error in connection database');
            action({
                type: 'conn',
                message: 'Connection Error From DB',
            }, null);
            conn.release();
            return;
        }

        conn.query(sql, function (err, result) {
            conn.release();
            if (err) {
                console.log('######### Syntax Error');
                console.log(sql);
                action({
                    type: 'syntax',
                    message: 'Syntax Error From DB',
                }, null);
                return;
            }
            log.queryCallResponse(result, sql, addr);
            action({type: 'success' }, result);
        });
    });
}

const req_select = function (obj) {
    query(obj.sql, obj.addr, function (err, result) {

        if(err.type==='conn' || err.type==='syntax') {
            obj.call_res.send({ err_message: err.message });
            return;
        }

        let list = [];
        result.forEach(function (item, index, array) {
            list.push(item);
        });

        if(obj.reverse)
            list.reverse();

        obj.call_res.send({
            err: undefined,
            totalCount: list.length,
            list: list
        });
    });
}

const req_insert = function (obj) {
    query(obj.sql, obj.addr, function (err, result) {

        if(err.type==='conn' || err.type==='syntax') {
            obj.call_res.send({ err_message: err.message });
            return;
        }
        obj.call_res.send({
            err: undefined,
            insert_id: result.insertId
        });
    });
}

const req_update = function (obj) {
    query(obj.sql, obj.addr, function (err, result) {

        if(err.type==='conn' || err.type==='syntax') {
            obj.call_res.send({ err_message: err.message });
            return;
        }

        obj.call_res.send();
    });
}

const req_delete = function (obj) {
    query(obj.sql, obj.addr, function (err, result) {

        if(err.type==='conn' || err.type==='syntax') {
            obj.call_res.send({ err_message: err.message });
            return;
        }

        obj.call_res.send();
    });
}

router.get('/req_aggregate', function(req, res) {

    grpc_aggregator_stub.aggregate({message: 'Nice to meet you!!'}, function (err, proto_res) {

        if (isErr(err))
            return

        if (existReponsedResult(proto_res))
            res.send(proto_res)

    });
});

router.get('/req_report', function(req, res) {

    grpc_aggregator_stub.report({message: 'Nice to meet you!!'}, function (err, proto_res) {

        if (isErr(err))
            return

        if (existReponsedResult(proto_res))
            res.send(proto_res)

    });
});

router.get('/req_collect', function(req, res) {

    grpc_collector_stub.collect({message: 'Nice to meet you!!'}, function (err, proto_res) {

        if (isErr(err))
            return

        if (existReponsedResult(proto_res))
            res.send(proto_res)

    });
});


router.get('/test_list', function(req, res) {
    req_select({
        "addr": "/test_list", "call_res": res, "reverse": false,
        "sql":`SELECT * FROM test`
    })
});

router.get('/insert_test', function(req, res) {
    req_insert({
        "addr": "/insert_test", "call_res": res, "reverse": false,
        "sql": `INSERT INTO test(d2, d3, d4) VALUES(123, 'aaabbb', NOW())`
    })
});

router.get('/update_test', function(req, res) {

    const d1_no = 5
    req_update({
        "addr": "/update_test", "call_res": res, "reverse": false,
        "sql": `UPDATE test SET d2=9999 WHERE d1=${d1_no}`
    })
});

router.get('/update_delete', function(req, res) {

    const d1_no = 5
    req_update({
        "addr": "/update_delete", "call_res": res, "reverse": false,
        "sql": `DELETE FROM test WHERE d1=${d1_no}`
    })
});

module.exports = router;