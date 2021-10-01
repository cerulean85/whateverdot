import os
import time

import config as cfg
import modules.collect.dir as dir

from modules.extractor.ExtractorTextNode import ExtractorTextNode
from modules.zhbase.ZHPickle import ZHPickle


def create_doc_text_blocks(work):
    # print(work)
    # print(len(work["model"]["content_ptp_list_path"]), len(work["model"]["taf_rank_path"]))

    channel = work["channel"]
    target_path = work["target_path"]
    file_name = work["file_name"]
    work_group_no = work["work_group_no"]
    work_no = work["work_no"]
    index = work["index"]
    keyword = work["keyword"]
    date= work["date"]
    save_path = work["save_dir"] + '/' + "{}_{}_{}_{}_{}_{}.csv".\
        format(channel, str(work_group_no), str(work_no), keyword, date, str(index))

    content_ptp_list = work["model"]["content_ptp_list_path"]
    taf_rank_dict = work["model"]["taf_rank_path"]
    taf_boundary_rank = work["model"]["taf_boundary_rank"]

    try:
        str_text_nodes = 'text,keyword,date\n'
        wd = ExtractorTextNode()
        items = wd.create_text_node_list(target_path + '/', file_name)
        for item in items:
            text = item["text"]
            ptp = item["ptp"]
            taf_rank = 1 if taf_rank_dict.get(text) is None else taf_rank_dict.get(text)
            if (ptp in content_ptp_list) and (taf_rank <= taf_boundary_rank):
                str_text_nodes += '{},{},{}\n'.format(text,keyword,date)
        print(str_text_nodes)

        with open(save_path, "w", encoding="utf-8") as f:
            f.write(str_text_nodes)

        print("Converted [{}]...".format(save_path))
    except Exception as e:
        print(e)


def work():
    conf = cfg.get_config(path=dir.config_path)
    save_dir = conf["storage"]["save_dir"]
    model_path = dir.model_path

    models = {}
    zhpk = ZHPickle()
    for path in os.listdir(model_path):
        channel = path
        if models.get(channel) is None:
            if conf["model"].get(channel) is not None:
                content_ptp_list_path = dir.model_path + channel + '/' + conf["model"][channel]["content_ptp_list"]
                taf_rank_path = dir.model_path + channel + '/' + conf["model"][channel]["taf_rank"]
                taf_boundary_rank = conf["model"][channel]["taf_boundary_rank"]

                models[channel] = {
                    "content_ptp_list_path": zhpk.load(content_ptp_list_path),
                    "taf_rank_path": zhpk.load(taf_rank_path),
                    "taf_boundary_rank": taf_boundary_rank
                }
    # print(models["nav"]["content_ptp_list_path"])
    # exit()

    last_index_check = {}
    d = []
    while True:
        for path, _, _ in os.walk(save_dir):
            if save_dir == path:
                continue

            if len(os.listdir(path)) > 0:
                if last_index_check.get(path) is None:
                    last_index_check[path] = 0

            file_list = os.listdir(path)
            file_list.sort(key=lambda x: (len(x), x))

            for file in file_list:
                if file == "converted":
                    continue

                tmp = file.split('.')
                tmp = tmp[0].split('_')
                channel = tmp[0]
                work_group_no = tmp[1]
                work_no = tmp[2]
                keyword = tmp[3]
                date = tmp[4]
                index = int(tmp[len(tmp)-1])
                if last_index_check[path] < index:
                    last_index_check[path] = index
                    d.append(index)
                    work = {
                        "channel": channel,
                        "work_group_no": work_group_no,
                        "work_no": work_no,
                        "keyword": keyword,
                        "date": date,
                        "index": index,
                        "target_path": path,
                        "file_name": file,
                        "save_dir": path + "/converted",
                        "model": models[channel]
                    }

                    create_doc_text_blocks(work)
                    # print(d)

        time.sleep(5)
        # print(file.split(.))


# file_path = conf["storage"]["save_dir"] + channel
# os.listdir(file_path)


work()
