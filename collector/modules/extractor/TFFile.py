import os


class TFFile:

    def make_dir(self, target_path):
        if not os.path.isdir(target_path):
            os.mkdir(target_path)

    def get_file_list(self, target_path):
        return os.listdir(target_path)

    def write_web_doc(self, target_path, filename, tb_data):
        self.make_dir(target_path)
        with open(target_path + filename, "w", encoding="utf-8") as f:
            for data in tb_data:
                f.write(data)

    def rename_files(self, target_path, file_rename):
        file_list = os.listdir(target_path)
        count = 1
        for file in file_list:
            if ".html" in file:
                os.rename(target_path + file, target_path + file_rename + str(count) + '.html')
                count += 1
