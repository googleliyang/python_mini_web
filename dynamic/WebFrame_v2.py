
# 封装一个函数,函数有一个参数，用来接收服务器传递 过来的客户请求址
import re

# wsgi的application 函数，有两个参数
# 参数一是一个字典，用来让服务器传递用户请求的信息,(其中一项就是客户端请求的地址)
# 参数二是一个函数引用，这个函数用来实现回调,回调的目的是用来将应用程序确的响应状态返回给服务器
def application(environ, start_response):

    # 通过参数一，取出客户端请的求地址
    file_name = environ['PATH_INFO']

    # 判断具体是哪个页面
    if file_name == '/index.py':
        # 访问的是首页

        # 拼接模板文件路径
        # 模板的作用，提供一个用来显示数据的格式
        path = './templates/index.html'

        # 读取模板文件内容
        with open(path, 'r') as file:
            file_content = file.read()

        # 替换
        # 准备一条假数据
        row_str = """ 
                <tr>
                    <td>1</td>
                    <td>000007</td>
                    <td>全新好</td>
                    <td>10.01%</td>
                    <td>4.40%</td>
                    <td>16.05</td>
                    <td>14.60</td>
                    <td>2017-07-18</td>
                    <td>
                        <input type="button" value="添加" id="toAdd" name="toAdd" systemidvaule="000007">
                    </td>
                </tr>  """
        # 将数据多弄几条
        all_data = ''
        for i in range(20):
            all_data += row_str

        # 使用数据替换模板中的占位符
        # 利用正则实现替换
        file_content = re.sub(r'\{%content%\}',all_data,file_content)




    elif file_name == '/center.py':
        # 访问的是个人中心页面

        # 响应体
        body = '<h1>Center Page Run v1</h1>'

    else:
        # 访问的是任意页面

        # 响应体
        body = '<h1>Other Page Run v1</h1>'

    # 通过传入的回调函数，来将响应状态返回给服务器,方便服务器进行拼接响应报文
    start_response('200 OK', [('Content-Type', 'text/html')])

    # 将数据返回
    return file_content

