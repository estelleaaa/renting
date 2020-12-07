# manage.py 作为启动文件 仅反应启动的流程 只需求把flask程序启动起来即可

from flask_session import Session
from flask_wtf import CSRFProtect
import redis

from app import create_app, db

# 创建flask应用对象
app = create_app('develop')

# 利用flask session 将session数据保存到redis中
Session(app)
# 为flask补充csrf防护机制
CSRFProtect(app)

@app.route("/index")
def index():
    return "index page"

if __name__ == '__main__':
    app.run()