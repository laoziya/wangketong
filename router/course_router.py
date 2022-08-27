from operator import and_
from flask import Blueprint, request
from sqlalchemy import or_, and_
from libs.userControl import User
from model import db
from libs.response import generate_response
from model.course import Course
from model.user_to_course import User_to_course
from libs.utils import format_dt
from flask_restful import Resource, Api









class CourseView(Resource):
    # 查找课程
    def get(self, cid=None):
        # url带cid，按照cid查找
        if cid:
            course = Course.query.get(cid)
            return generate_response(message='course query success', data=dict(course))
            
        # 按照关键字查找
        keyword = request.args.get('keyword')
        uid = request.args.get('uid')
        if not keyword and not uid:
            return generate_response(status_code=1001, message='missing query parame')
        if keyword:
            c_lst = Course.query.filter(or_(
                Course.cname.like(f'%%{keyword}%%'),
                Course.desc.like(f'%%{keyword}%%')
            )).all()
            result = []
            for c in c_lst:
                # tmp = {**dict(c), **dict(c.user)}
                # tmp["CreateAt"] = str(tmp.get("CreateAt"))
                # result.append(tmp)

                c_dict = dict(c)
                user_dict = dict(c.user)
                c_dict["CreateAt"] = str(c_dict.get("CreateAt"))
                c_dict['user'] = user_dict
                c_dict['star'] = len(c.m)
                result.append(c_dict)
            return generate_response(message='course query success', data=result)
        if uid: # 查找某个用户的所有课程
            course_lst = Course.query.filter(Course.uid==uid).all()
            result = []
            for c in course_lst:
                c_dict = dict(c)
                c_dict['star'] = len(c.m)
                c_dict['CreateAt'] = str(c_dict['CreateAt'])
                result.append(c_dict)
            return generate_response(message='course get success', data=result)

    # 新建课程
    def post(self):
        # 先验证，通过cookie得到uid
        uid = 3
        # 验证通过后就执行以下操作
        cname= request.form.get('cname')
        desc = request.form.get('desc')
        if not cname:
            return generate_response(status_code=1001, message='course name is null')
        if Course.query.filter(and_(Course.cname==cname, Course.uid==uid)).first():
            return generate_response(status_code=1001, message='course is exists')
        course = Course()
        course.cname = cname
        course.uid = uid
        if desc:
            course.desc = desc
        db.session.add(course)
        db.session.commit()
        return generate_response(message='create course success')

    # 修改课程
    def put(self, cid):
        if not cid:
            return generate_response(status_code=10001, message='missing cid')
        cname = request.form.get('cname')
        desc = request.form.get('desc')
        course = Course.query.get(cid)
        if not course:
            return generate_response(status_code=10001, message='course not found')
        msg = 'course msg mod success'
        status_code = 10000
        if cname:
            if course.cname != cname:
                course.cname = cname
            else:
                msg = 'not modify'
                status_code = 10000
        if desc:
            if course.desc != desc:
                course.desc = desc
            else:
                msg = 'not modify'
                status_code = 10000
        db.session.add(course)
        db.session.commit()
        return generate_response(status_code=status_code,message=msg)
    
    # 删除课程
    def delete (self, cid):
        if not cid:
            return generate_response(status_code=10001, message='missing cid')
        course = Course.query.get(cid)
        if not course:
            return generate_response(status_code=10001, message='course not found')
        db.session.delete(course)
        db.session.commit()
        return generate_response(message='course delete success')



class StarCourseView(Resource):
    # 查找指定uid用户收藏的课程：GET: /course/star/<int:uid>
    def get(self, id=None):
        record_lst = User_to_course.query.filter(User_to_course.uid==id).all()
        result = []
        for record in record_lst:
            course = dict(record.course)
            course['CreateAt'] = str(course['CreateAt'])
            result.append(course)
        return generate_response(message='success', data=result)
    # 收藏课程：POST: /course/star/<int:cid>
    def post(self, id):
        uid = 6
        cid = id
        if not Course.query.get(cid):
            return generate_response(status_code=1001, message='no found this course')
        exist_status = User_to_course.query.filter(and_(
            User_to_course.cid == cid,
            User_to_course.uid == uid
        )).first()
        if exist_status:
            return generate_response(status_code = 1001, message='course exists')
        record = User_to_course()
        record.uid = uid
        record.cid = cid
        db.session.add(record)
        db.session.commit()
        return generate_response(message='add course success')
    
    # 退出课程：DELETE: /course/star/<int:cid>
    def delete (self, id):
        uid = 6
        cid = id
        record_lst = User_to_course.query.filter(and_(
            User_to_course.cid == cid,
            User_to_course.uid == uid
        ))
        for record in record_lst:
            db.session.delete(record)
        db.session.commit()
        return generate_response(message="exit course success")



class ManagerFansView(Resource):
    # 查找一个课程中所有的用户
    def get(self, cid=None):
       user_lst = User_to_course.query.filter(User_to_course.cid==cid).all()
       return generate_response(message='success', data=[dict(user.user) for user in user_lst])
    # 将某个用户踢出课程
    def delete (self, cid):
        uid = request.args.get('uid')
        if not uid:
            return generate_response(status_code=10001, message="missing parame")
        record_lst = User_to_course.query.filter(and_(
            User_to_course.cid == cid,
            User_to_course.uid == uid
        )).all()
        if not record_lst:
            return generate_response(status_code=10001, message="not exists user")
        for record in record_lst:
            db.session.delete(record)
        db.session.commit()
        return generate_response(message="delete fans success")




# 新建蓝图
from flask import Blueprint

course_bp = Blueprint('course', __name__, url_prefix='/api/course')

# api
course_api = Api(course_bp)
# 用户管理课程（新建课程，删除课程，查找课程）
course_api.add_resource(CourseView, '/')
course_api.add_resource(CourseView, '/<int:cid>', endpoint='course_api_p')

# 课程收藏方面的操作（查询出所有收藏课程，收藏，退出课程）
course_api.add_resource(StarCourseView, '/star')
course_api.add_resource(StarCourseView, '/star/<int:id>', endpoint = 'StarCourseView_id')
# course_api.add_resource(StarCourseView, '/star/<int:cid>', endpoint = 'StarCourseView_cid')

# 管理课程中的用户
course_api.add_resource(ManagerFansView, '/user/<int:cid>')

