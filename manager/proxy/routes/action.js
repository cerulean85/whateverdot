var express = require("express")
var router = express.Router();
const config = require("../config");
const cors = require("cors");
const grpc = require("../routes/stub");
const query = require("../routes/query");
const util = require("../routes/util");

function strNull(v) {
    if(v===undefined || v==='undefined') return '';
    return v;
}

router.get('/echo', function(req, res) {
   grpc.stub.echo(res, req, function (err, proto_res) {
       if (grpc.existReponsedResult(proto_res, err))
           return res.send(proto_res)
   })
});

function generateKeywords(keywords, key_opts) {
    let currentKeywordIndex = 0
    const split_keywords = keywords.split(',')
    const split_key_opts = key_opts.split(',')

    let currentKeywords = [split_keywords[currentKeywordIndex]]
    for(var index=0; index<split_key_opts.length; index++) {
        currentKeywordIndex++;
        const targetKeyword = split_keywords[currentKeywordIndex]
        const opt = split_key_opts[index]
        let refreshedKeywords = [];
        if(opt === "AND") {
            for(var jdex=0; jdex<currentKeywords.length; jdex++) {
                refreshedKeywords.push(currentKeywords[jdex] + ' ' + targetKeyword)
            }
            currentKeywords = refreshedKeywords;
        }
        if(opt === "OR") {
            console.log(opt)
            for(var jdex=0; jdex<currentKeywords.length; jdex++) {
                refreshedKeywords.push(currentKeywords[jdex])
                refreshedKeywords.push(currentKeywords[jdex] + ' ' + targetKeyword)
            }
            currentKeywords = refreshedKeywords;
        }
    }

    return currentKeywords
}

router.get("/enroll_works", function(req, res){
    req = {
        title: "Test",
        keywords: "A,B,C,D,X",
        key_opts: "AND,OR,OR,AND",
        channels: "nav,jna,twt,ins",
        start_dt: "2020-01-01",
        end_dt: "2020-01-30"
    };

    query.query_insert({
        "addr": "/insert_work_group", "call_res": res, "reverse": false, "res_send": true,
        "sql": `INSERT INTO work_groups(title, keywords, channels, start_dt, end_dt)
                VALUES('${req.title}', '${req.keywords}', '${req.channels}', '${req.start_dt}', '${req.end_dt}')`,
        "emit": function (result) {
            const workGroupNo = result.insertId
            const genKeywords = generateKeywords(req.keywords, req.key_opts)
            const splitChannels = req.channels.split(',')

            let sql = `INSERT INTO works(work_group_no, keyword, channel, start_dt, end_dt) VALUES`
            for(const keyword of genKeywords) {
                for(const channel of splitChannels) {
                    sql += `('${workGroupNo}', '${keyword}', '${channel}', '${req.start_dt}', '${req.end_dt}'),`
                }
            }
            sql = sql.slice(0, -1)

            query.query_insert({
                "addr": "/insert_works", "call_res": res, "reverse": false, "res_send": false,
                "sql": sql, "emit": undefined
            });

        }
    });
})

router.get('/collect_urls', function(req, res) {
    req = { groupNo: 9 }
    query.query_select({
        "addr": "/req_collect_urls", "call_res": res, "reverse": false, "res_send": false,
        "sql": `SELECT * FROM works WHERE work_group_no=${req.groupNo}`,
        "emit": function(result) {
            console.log("오잉")

            let workList = []
            for (const work of result) {
                workList.push({
                    "no": work.work_no,
                    "groupNo": work.work_group_no,
                    "keywords": [work.keyword],
                    "channels": [work.channel],
                    "collectionDates": [util.dateFormatting(work.start_dt), util.dateFormatting(work.end_dt)]
                })
            }
            console.log(workList)
            grpc.stub.collectUrls({ workList: workList }, req, function (err, proto_res) {
                // console.log(res)
                if (grpc.existReponsedResult(proto_res, err))
                    return res.send(proto_res)
            })
        }
    })
});

// router.get('/req_aggregate', function(req, res) {
//
//     stub.aggregate({message: 'Nice to meet you!!'}, function (err, proto_res) {
//
//         if (isErr(err))
//             return
//
//         if (existReponsedResult(proto_res))
//             res.send(proto_res)
//
//     });
// });
//
// router.get('/req_report', function(req, res) {
//
//     stub.report({message: 'Nice to meet you!!'}, function (err, proto_res) {
//
//         if (isErr(err))
//             return
//
//         if (existReponsedResult(proto_res))
//             res.send(proto_res)
//
//     });
// });
//

//
// router.get('/req_collect_docs', function(req, res) {
//
//     req = {
//         no: 1,
//         groupNo: 101,
//         keywords: ["A", "B", "C"],
//         channels: ["nav", "jna", "twt", "ins"],
//         message: "req_collect"
//     }
//     stub.collectDocs({message: 'Nice to meet you!!'}, function (err, proto_res) {
//
//         if (isErr(err))
//             return
//
//         if (existReponsedResult(proto_res))
//             res.send(proto_res)
//
//     });
// });
//
//
// router.get('/test_list', function(req, res) {
//     req_select({
//         "addr": "/test_list", "call_res": res, "reverse": false,
//         "sql":`SELECT * FROM test`
//     })
// });
//
// router.get('/insert_test', function(req, res) {
//     req_insert({
//         "addr": "/insert_test", "call_res": res, "reverse": false,
//         "sql": `INSERT INTO test(d2, d3, d4) VALUES(123, 'aaabbb', NOW())`
//     })
// });
//
// router.get('/update_test', function(req, res) {
//
//     const d1_no = 5
//     req_update({
//         "addr": "/update_test", "call_res": res, "reverse": false,
//         "sql": `UPDATE test SET d2=9999 WHERE d1=${d1_no}`
//     })
// });
//
// router.get('/update_delete', function(req, res) {
//
//     const d1_no = 5
//     req_update({
//         "addr": "/update_delete", "call_res": res, "reverse": false,
//         "sql": `DELETE FROM test WHERE d1=${d1_no}`
//     })
// });

module.exports = router;