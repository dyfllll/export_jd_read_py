导出京东阅读已购买的电子书

## 如何使用

### 下载代码, 并安装依赖

1. 克隆 repo
2. 安装 Python 虚拟环境
3. 安装 requirements.txt 中的依赖

**示例脚本：**

```
git clone https://github.com/dyfllll/export_jd_read_py.git
cd export_jd_read_py
python -m venv venv
CALL venv\Scripts\activate.bat
pip install -r requirements.txt
```

### 登录保存cookies

第一次需要，之后就直接使用，有可能cookies会失效，失效就删掉重新生成

1. 运行main.py
2. 在弹出的网页中登录
3. 打开书架中的一本书，将翻页方式改为**`上下翻页`**
4. 在命令行中按回车，生成cookies.json

### 导出html版本

1. 将要下载的`bookId`添加到main.py中Download_Book_List中，[bookId获取方法](https://github.com/goodwjf/export_jd_read)
2. 运行main.py，会自动下载书籍到`output` 目录

### 缓存图片资源

因为html里面图片是url链接形式，必须在线使用，所以可以把图片资源缓存在本地：

1. 运行downloadHtmlAsset.py，输入1，导出所有要下载的图片到`output/download.json`，并替换html里面图片地址
2. 运行downloadHtmlAsset.py，输入2，下载所有图片到本地

### 生成PDF

生成pdf需要安装[wkhtmltopdf.exe](https://wkhtmltopdf.org/downloads.html)，安装后替换html2pdf.py中wkhtmltopdf.exe安装地址

```python
config = pdfkit.configuration(
    wkhtmltopdf="D:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"
)
```

运行html2pdf.py生成pdf

最后生成PDF是否带书签目录根据wkhtmltopdf.exe生成的单个PDF是否带书签目录决定的

### 其他

`main.py`中`save_catalog`函数是根据`Reader.$children[0].$children[0].catalogArr`获取目录数据结构，这段代码是使用`JS Digger`查找出来的，后面可能失效,如果失效自己使用`JS Digger`重新查找



