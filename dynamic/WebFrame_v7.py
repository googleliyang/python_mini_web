
# 封装一个函数,函数有一个参数，用来接收服务器传递 过来的客户请求址
import re
from pymysql import *


# 定义一个用来维护请求地址和响应函数字典，作为路由表
router_table = {}



# 定义一可以接收参数的装饰器，实现自动维护向路由表中去添加键值对
def router(url):
    def wrapper(func):
        def inner(*args, **kwargs):
            # 执行被装饰函数,并且要要返回被装饰函数的返回值
            return func(*args, **kwargs)
        # 在这里，利用router 函数接收的url做为key，将inner 函数做为值，保存到路由字典中
        router_table[url] = inner
        print(router_table)
        return inner
    return wrapper

# wsgi的application 函数，有两个参数
# 参数一是一个字典，用来让服务器传递用户请求的信息,(其中一项就是客户端请求的地址)
# 参数二是一个函数引用，这个函数用来实现回调,回调的目的是用来将应用程序确的响应状态返回给服务器
def application(environ, start_response):

    # 通过参数一，取出客户端请的求地址
    file_name = environ['PATH_INFO']

    # 判断具体是哪个页面

    # 先定义一个函数引用，用来记录other
    func = other

    # 通过字典查找请求地址对应的响应函数
    if file_name in router_table:
        func = router_table[file_name]

    # 执行函数调用,并要接收返回的数据
    file_content = func()

    # 通过传入的回调函数，来将响应状态返回给服务器,方便服务器进行拼接响应报文
    start_response('200 OK', [('Content-Type', 'text/html')])

    # 将数据返回
    return file_content


def other():
    # 响应体
    file_content = '<h1>Other Page Run v5</h1>'
    return file_content

@router('/center.html')  # center = inner
def center():
    path = './templates/center.html'
    with open(path, 'r') as file:
        file_content = file.read()
    row_str = """ 
            <tr>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>
                    <a type="button" class="btn btn-default btn-xs" href="/update/%s.html"> <span class="glyphicon glyphicon-star" aria-hidden="true"></span> 修改 </a>
                </td>
                <td>
                    <input type="button" value="删除" id="toDel" name="toDel" systemidvaule="%s">
                </td>
            </tr> """

    # 读取数据库
    db_connect = Connect(host='localhost',port=3306,database='stock_db',user='root',password='123123',charset='utf8')
    cur = db_connect.cursor()
    sql_str = ''' select info.code,info.short,info.chg,info.turnover,info.price,info.highs,focus.note_info from focus left join info on focus.info_id = info.id; '''
    cur.execute(sql_str)
    result = cur.fetchall()
    cur.close()
    db_connect.close()

    # 准备一个数据
    all_data = ''
    for t in result:
        all_data += row_str % (t[0],t[1],t[2],t[3],t[4],t[5],t[6],t[0],t[0])

    # 替换模板文件内容
    file_content = re.sub(r'\{%content%\}', all_data, file_content)
    return file_content

@router('/index.html')
def index():
    # 拼接模板文件路径
    # 模板的作用，提供一个用来显示数据的格式
    path = './templates/index.html'
    # 读取模板文件内容
    with open(path, 'r') as file:
        file_content = file.read()

    # 替换
    # 准备一条数据格式字符串
    row_str = """ 
                <tr>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>
                        <input type="button" value="添加" id="toAdd" name="toAdd" systemidvaule="%s">
                    </td>
                </tr>  """

    # 读取数据库
    db_connect = Connect(host='localhost',port=3306,database='stock_db',user='root',password='123123',charset='utf8')
    cur = db_connect.cursor()
    sql_str = ''' select * from info '''
    cur.execute(sql_str)
    result = cur.fetchall()
    cur.close()
    db_connect.close()


    # 将数据库里读取的数据，替换到格式字符串中
    all_data = ''
    for t in result:
        all_data += row_str % (t[0],t[1],t[2],t[3],t[4],t[5],t[6],t[7],t[1])


    # 使用替换完成后的数据替换模板中的占位符
    # 利用正则实现替换
    file_content = re.sub(r'\{%content%\}', all_data, file_content)
    return file_content

@router('/login.html')
def login():
    return 'Login Page Run ...'

