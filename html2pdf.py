import pdfkit
import os
import json
from PyPDF2 import PdfMerger, PdfReader, PdfWriter

Data_Folder = "./output"

# pdfkit需要安装wkhtmltopdf
config = pdfkit.configuration(
    wkhtmltopdf="D:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"
)
# 添加 wkhtmltopdf 配置选项
options = {"enable-local-file-access": None}  # 允许访问本地文件


#TODO 目录根据导出json设置目录
def merge_pdfs_with_bookmarks(pdf_files, output_file):
    """
    合并多个 PDF 文件，并使用单个 PDF 文件的书签。

    参数:
    - pdf_files: PDF 文件路径列表。
    - output_file: 输出合并后的 PDF 文件路径。
    """
    writer = PdfWriter()
    total_pages = 0  # 用于计算书签的页码偏移量

    for i, file_path in enumerate(pdf_files):
        reader = PdfReader(file_path)

        # 将当前 PDF 的页面添加到输出文件中
        for page in reader.pages:
            writer.add_page(page)

        # 如果当前 PDF 是指定的书签来源
        def add_bookmarks(bookmarks, parent=None):
            last_bookmark = None
            for bookmark in bookmarks:
                if isinstance(bookmark, list):
                    # 处理嵌套书签
                    add_bookmarks(bookmark, last_bookmark)
                else:
                    # 添加书签（页码需要加上偏移量）
                    last_bookmark = writer.add_outline_item(
                        title=bookmark.title,
                        page_number=bookmark.page + total_pages,
                        parent=parent,
                    )

        add_bookmarks(reader.outline)

        # 更新总页码偏移量
        total_pages += len(reader.pages)

    # 保存输出文件
    with open(output_file, "wb") as output_pdf:
        writer.write(output_pdf)
    print(f"PDF 合并完成！输出文件为：{output_file}")


def bookToPdf(name, folder):
    targetPath = os.path.join(Data_Folder, f"{name}.pdf")
    if os.path.exists(targetPath):
        print(f"{targetPath}已存在,跳过生成")
        return

    html_folder = os.path.join(folder, "Data")
    pdf_folder = os.path.join(html_folder, "pdf")
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)

    json_path = os.path.join(folder, "index.json")
    if not os.path.exists(json_path):
        print(f"{json_path}不存在,跳过生成")
        return

    with open(json_path, "r") as f:
        jsonArray = json.load(f)
    pdfs = []
    last_chapter_item = ""
    for i, it in enumerate(jsonArray):
        chapter_item = it["chapter_item"]  # +".html"
        if chapter_item != last_chapter_item:
            html_path = os.path.join(html_folder, chapter_item)
            pdf_path = os.path.join(pdf_folder, f"{chapter_item}.pdf")
            # try:
            pdfkit.from_file(html_path, pdf_path, configuration=config, options=options)
            # except Exception as e:
            #     ...
            pdfs.append(pdf_path)
            last_chapter_item = chapter_item
        print(f"{i+1}/{len(jsonArray)} 生成:{pdf_path}")

    merge_pdfs_with_bookmarks(pdfs, targetPath)
    # file_merger = PdfMerger()
    # for pdf in pdfs:
    #     file_merger.append(pdf)
    # file_merger.write(targetPath)

    print(f"生成成功:{targetPath}")


def main():
    items = os.listdir(Data_Folder)
    for item in items:
        full_path = os.path.join(Data_Folder, item)
        if os.path.isdir(full_path):
            bookToPdf(item, full_path)


if __name__ == "__main__":
    main()
