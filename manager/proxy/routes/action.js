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

router.post('/echo', function(req, res) {
   grpc.stub.echo(res, req, function (err, proto_res) {
       if (grpc.existReponsedResult(proto_res, err))
           return res.send(proto_res)
   })
});

function generateKeywords(keywords, key_opts) {
    let currentKeywordIndex = 0

    const split_keywords = keywords.length === 1 ? keywords[0] : keywords.split(',')
    const split_key_opts = key_opts.length === 1 ? key_opts[0] : key_opts.split(',')

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

router.post("/get_work_group_list", function(req, res){
    // req = {
    //     title: "Test",
    //     keywords: "A,B,C,D,X",
    //     key_opts: "AND,OR,OR,AND",
    //     channels: "nav,jna,twt,ins",
    //     start_dt: "2020-01-01",
    //     end_dt: "2020-01-30"
    // };
    query.query_select({
        "addr": "/get_work_group_list", "call_res": res, "reverse": false, "res_send": true,
        "sql": `SELECT * FROM work_groups WHERE deleted = 0`,
        "emit": function (result) {
            let workGroupList = []
            for (const workGroup of result) {
                workGroupList.push({
                    "title": workGroup.title,
                    "work_group_no": workGroup.work_group_no,
                    "keywords": workGroup.keywords,
                    "channels": workGroup.channels,
                    "start_date": util.dateFormatting(workGroup.start_dt),
                    "end_date": util.dateFormatting(workGroup.end_dt),
                    "work_state": workGroup.work_state
                })
            }
            console.log(workGroupList)
            res.send({
                err_message: undefined,
                totalCount: workGroupList.length,
                list: workGroupList
            })
        }
    });
})

router.post("/enroll_works", function(req, res){
    // req = {
    //     title: "Test",
    //     keywords: "A,B,C,D,X",
    //     key_opts: "AND,OR,OR,AND",
    //     channels: "nav,jna,twt,ins",
    //     start_dt: "2020-01-01",
    //     end_dt: "2020-01-30"
    // };
    query.query_insert({
        "addr": "/enroll_works", "call_res": res, "reverse": false, "res_send": true,
        "sql": `INSERT INTO work_groups(title, keywords, key_opts, channels, start_dt, end_dt, work_state)
                VALUES('${req.body.title}', '${req.body.keywords}', '${req.body.key_opts}', '${req.body.channels}', '${req.body.start_dt}', '${req.body.end_dt}', 'waiting')`,
        "emit": function (result) {
            // const workGroupNo = result.insertId
            // const genKeywords = generateKeywords(req.body.keywords, req.body.key_opts)
            // const splitChannels = req.body.channels.split(',')
            //
            // let sql = `INSERT INTO works(work_group_no, keyword, channel, start_dt, end_dt) VALUES`
            // for(const keyword of genKeywords) {
            //     for(const channel of splitChannels) {
            //         sql += `('${workGroupNo}', '${keyword}', '${channel}', '${req.body.start_dt}', '${req.body.end_dt}'),`
            //     }
            // }
            // sql = sql.slice(0, -1)
            //
            // query.query_insert({
            //     "addr": "/insert_works", "call_res": res, "reverse": false, "res_send": false,
            //     "sql": sql, "emit": undefined
            // });
        }
    });
})

router.post("/route_monitor", function(req, res){

})

// router.get('/collect_urls', function(req, res) {
//     req = { groupNo: 9 }
//     query.query_select({
//         "addr": "/req_collect_urls", "call_res": res, "reverse": false, "res_send": false,
//         "sql": `SELECT * FROM works WHERE work_group_no=${req.groupNo}`,
//         "emit": function(result) {
//
//             let workList = []
//             for (const work of result) {
//                 workList.push({
//                     "no": work.work_no,
//                     "groupNo": work.work_group_no,
//                     "keywords": [work.keyword],
//                     "channels": [work.channel],
//                     "collectionDates": [util.dateFormatting(work.start_dt), util.dateFormatting(work.end_dt)]
//                 })
//             }
//             console.log(workList)
//             grpc.stub.collectUrls({ workList: workList }, req, function (err, proto_res) {
//                 if (grpc.existReponsedResult(proto_res, err))
//                     return res.send(proto_res)
//             })
//         }
//     })
// });
//
// router.get('/collect_docs', function(req, res) {
//     req = { groupNo: 9 }
//     query.query_select({
//         "addr": "/req_collect_docs", "call_res": res, "reverse": false, "res_send": false,
//         "sql": `SELECT * FROM works WHERE work_group_no=${req.groupNo}`,
//         "emit": function(result) {
//
//             let workList = []
//             for (const work of result) {
//                 workList.push({
//                     "no": work.work_no,
//                     "groupNo": work.work_group_no,
//                     "keywords": [work.keyword],
//                     "channels": [work.channel],
//                     "collectionDates": [util.dateFormatting(work.start_dt), util.dateFormatting(work.end_dt)]
//                 })
//             }
//             console.log(workList)
//             grpc.stub.collectDocs({ workList: workList }, req, function (err, proto_res) {
//                 if (grpc.existReponsedResult(proto_res, err))
//                     return res.send(proto_res)
//             })
//         }
//     })
// });
//
// router.get('/extract_texts', function(req, res) {
//     req = { groupNo: 9 }
//     query.query_select({
//         "addr": "/req_extract_texts", "call_res": res, "reverse": false, "res_send": false,
//         "sql": `SELECT * FROM works WHERE work_group_no=${req.groupNo}`,
//         "emit": function(result) {
//
//             let workList = []
//             for (const work of result) {
//                 workList.push({
//                     "no": work.work_no,
//                     "groupNo": work.work_group_no,
//                     "keywords": [work.keyword],
//                     "channels": [work.channel],
//                     "collectionDates": [util.dateFormatting(work.start_dt), util.dateFormatting(work.end_dt)]
//                 })
//             }
//             console.log(workList)
//             grpc.stub.extractTexts({ workList: workList }, req, function (err, proto_res) {
//                 if (grpc.existReponsedResult(proto_res, err))
//                     return res.send(proto_res)
//             })
//         }
//     })
// });
//
// router.get('/extract_contents', function(req, res) {
//     req = { groupNo: 9 }
//     query.query_select({
//         "addr": "/req_extract_contents", "call_res": res, "reverse": false, "res_send": false,
//         "sql": `SELECT * FROM works WHERE work_group_no=${req.groupNo}`,
//         "emit": function(result) {
//
//             let workList = []
//             for (const work of result) {
//                 workList.push({
//                     "no": work.work_no,
//                     "groupNo": work.work_group_no,
//                     "keywords": [work.keyword],
//                     "channels": [work.channel],
//                     "collectionDates": [util.dateFormatting(work.start_dt), util.dateFormatting(work.end_dt)]
//                 })
//             }
//             console.log(workList)
//             grpc.stub.extractContents({ workList: workList }, req, function (err, proto_res) {
//                 if (grpc.existReponsedResult(proto_res, err))
//                     return res.send(proto_res)
//             })
//         }
//     })
// });

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