
import app

# 实例化一个Flask对象
# 实例化的时候传入import_name，通常使用__name__
myapp = app.create_app()

myapp.run(debug=myapp.config['DEBUG'], host=myapp.config['HOST'], port=myapp.config['PORT'])
