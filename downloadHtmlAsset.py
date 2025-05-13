import requests
import os
import re
import json

Data_Folder = "./output"


def getHtmlAsset(folder, filename, filePath, info, checkSet: set):
    with open(filePath, "r", encoding="utf-8") as file_W:
        content = file_W.read()

    pattern = r"https:\/\/\w+\.360buyimg\.com\/([^\"]+\.\w+)"
    # 找到所有匹配的地址
    matches = re.findall(pattern, content)
    if matches:
        # 备份原始html
        bak_folder = os.path.join(folder, "bak")
        if not os.path.exists(bak_folder):
            os.makedirs(bak_folder)
        with open(
            os.path.join(bak_folder, filename), "w", encoding="utf-8"
        ) as file_bak:
            file_bak.write(content)

        def replacer(match):
            file_name = "asset/" + match.group(1).replace("/", "-")

            url = match.group(0)
            downloadPath = os.path.join(folder, file_name).replace("\\", "/")
            it_info = {}
            it_info["url"] = url
            it_info["path"] = downloadPath

            if not url in checkSet:
                info.append(it_info)
                checkSet.add(url)
                
            return f"./{file_name}"

        # 替换地址为新的 URL
        content = re.sub(pattern, replacer, content)
        with open(filePath, "w", encoding="utf-8") as file_W:
            file_W.write(content)


def getBookAsset(folder, info):
    html_folder = os.path.join(folder, "Data")
    items = os.listdir(html_folder)
    checkSet = set()
    for item in items:
        full_path = os.path.join(html_folder, item)
        if os.path.isfile(full_path):
            getHtmlAsset(html_folder, item, full_path, info, checkSet)


def exportDownloadJson():
    info = []
    items = os.listdir(Data_Folder)

    for item in items:
        full_path = os.path.join(Data_Folder, item)
        if os.path.isdir(full_path):
            getBookAsset(full_path, info)

    with open(os.path.join(Data_Folder, "download.json"), "w") as f:
        json.dump(info, f, indent=4)  


def downloadAsset():
    jsonPath = os.path.join(Data_Folder, "download.json")
    if not os.path.exists(jsonPath):
        print("download.json不存在")
        return
    with open(jsonPath, "r") as f:
        jsonArray = json.load(f)

    total = len(jsonArray)
    print(f"total: {total}")
    errorArray = []
    index = 0

    try:
        for it in jsonArray:
            url = it["url"]
            path = it["path"]
            try:
                dir_path = os.path.dirname(path)
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                response = requests.get(url)
                if not response.ok:
                    raise IOError("下载失败")
                with open(path, "wb") as file:
                    file.write(response.content)
                print(f"{index+1}/{total} 下载成功:{path}")
            except Exception as e:
                errorArray.append(it)
                print(f"{index+1}/{total} 下载失败:{path} url:{url}")
            index += 1

    finally:
        for i in range(index, total):
            errorArray.append(jsonArray[i])
        if len(errorArray) > 0:
            with open(os.path.join(Data_Folder, "error.json"), "w") as f:
                json.dump(errorArray, f, indent=4)
            print(f"已保存error.json")
        print(f"下载完成,下载失败个数:{len(errorArray)}")


def main():
    if not os.path.exists(Data_Folder):
        print("文件夹不存在")
        return
    user_input = input(
        """
                       请输入：
                       1 导出所有需要下载图片到output/download.json,并替换html里面链接
                       2 根据download.json下载图片,下载失败会生成error.json,把error.json改成download.json可继续下载
        """
    )
    if user_input == "1":
        exportDownloadJson()
    elif user_input == "2":
        downloadAsset()


if __name__ == "__main__":
    main()
