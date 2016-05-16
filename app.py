#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from json import loads, dumps
import requests
app = Flask(__name__)

@app.route('/')
def index():
    return """<html>
    <head>
        <title>Course API
        </title>
    </head>
    <body>
        <h2>Pycourses is a MOOC API . </h2>
        <h3>To utilise thi API properly you'll need to follow the syntax mentioned below :-</h3>
        <br>
        <p>1  To extract details of a particular course :-<br><br>
                    url:- /course/api/v1.0/courses/course_name<br><br>
            2  To extract details of a particular course from a particular MOOC site  :-<br><br>
                     url:- /course/api/v1.0/courses/provider/course_name<br><br>
                       !!NOTE presently providers are - Coursera,Udemy,Udacity
                  <br><br>
             3  To extract all courses from coursera :-<br><br>
                     url:- /course/api/v1.0/courses/coursera?start="start results from this number"&limit="number of results to display on a page"
                  <br><br>
             4  To extract details of all courses from udacity :-<br><br>
                     url:- /course/api/v1.0/courses/udacity<br><br>
             5  To extract details of all courses from udemy :-<br><br>
                    url:-  /course/api/v1.0/courses/udemy?pagesize="number of results to display on page"<br>
        </body>
</html>"""


@app.route('/course/api/v1.0/courses/coursera', methods=['GET'])
def AllCourseFromCoursera():
    start = request.args.get('start')
    limit = request.args.get('limit')
    coursera = coursera_all_courses(start, limit)
    c={"courses":coursera}
    return dumps(c,indent=4, sort_keys=True)


@app.route('/course/api/v1.0/courses/udacity', methods=['GET'])
def AllCourseFromUdacity():
    udacity = udacity_all_courses()
    c={"courses":udacity}
    return dumps(c,indent=4, sort_keys=True)


@app.route('/course/api/v1.0/courses/udemy', methods=['GET'])
def AllCourseFromUdemy():
    size = request.args.get('size')
    udemy = udemy_all_courses(size)
    c={"courses":udemy}
    return dumps(c,indent=4, sort_keys=True)


@app.route('/course/api/v1.0/courses/<string:course_name>',
           methods=['GET'])
def CourseFromAllProviders(course_name, charset='utf-8'):
    coursera = coursera_course(course_name)
    udemy = udemy_course(course_name)
    udacity = udacity_course(course_name)
    x = coursera+udemy+udacity
    c={"courses":x}
    return dumps(c,indent=4, sort_keys=True)


@app.route('/course/api/v1.0/courses/<string:provider_name>/<string:course_name>'
           , methods=['GET'])
def CourseFromProvider(course_name, provider_name):
    if provider_name.lower() == 'coursera':
        coursera = coursera_course(course_name)
        c={"courses":coursera}
        return dumps(c,indent=4, sort_keys=True)
    if provider_name.lower() == 'udemy':
        udemy = udemy_course(course_name)
        c={"courses":udemy}
        return dumps(c,indent=4, sort_keys=True)
    if provider_name.lower() == 'udacity':
        udacity = udacity_course(course_name)
        c={"courses":udacity}
        return dumps(c,indent=4, sort_keys=True)


def coursera_store_course(item):
    name = item['name']
    type = item['courseType']
    slug = item['slug']

    if 'v2' in type:
        course_url = 'https://www.coursera.org/learn/' + slug
    else:
        course_url = 'https://www.coursera.org/course/' + slug

    description = item['description']
    course = {
        'name': name,
        'url': course_url,
        'description': description,
        'provider': 'coursera',
        'price': 'Null',
        }
    return course


def coursera_course(course):
    coursera_courses = []
    url_params = 'slug,courseType,primaryLanguages,description'
    url = 'https://api.coursera.org/api/courses.v1?q=search&query=' \
        + course + ',primaryLanguages=[%22en%22]&fields=' + url_params
    res = requests.get(url)
    results = res.text
    json_result = loads(results)
    for item in json_result['elements']:
        if 'en' in item['primaryLanguages']:
            coursera_courses.append(coursera_store_course(item))

    return coursera_courses


def coursera_all_courses(start, limit):
    if not start:
        start = 1
    if not limit:
        limit = 100
    coursera_all_courses = []
    url_params = 'slug,courseType,primaryLanguages,description'

    url = 'https://api.coursera.org/api/courses.v1?start=' + str(start) \
        + '&limit=' + str(limit) + '&fields=' + url_params
    res = requests.get(url)
    results = res.text
    json_result = loads(results)
    for item in json_result['elements']:
        if 'en' in item['primaryLanguages']:
            coursera_all_courses.append(coursera_store_course(item))

    return coursera_all_courses


def udacity_store_course(item, course2):
    name = item['title']
    url = item['homepage']
    course2=course2.lower()
    course = {}
    if course2 in item['summary'].lower():
        description = "Null"
        course = {
            'name': name,
            'url': url,
            'description': description,
            'provider': 'udacity',
            'price': 'Null',
            }
        return course
    elif course2 in item['syllabus'].lower():
        description = "Null"
        course = {
            'name': name,
            'url': url,
            'description': description,
            'provider': 'udacity',
            'price': 'Null',
            }
        return course
    elif course2 in item['short_summary'].lower():
        description = "Null"
        course = {
            'name': name,
            'url': url,
            'description': description,
            'provider': 'udacity',
            'price': 'Null',
            }
        return course    
    elif course2 in item['expected_learning'].lower():
        description = "Null"
        course = {
            'name': name,
            'url': url,
            'description': description,
            'provider': 'udacity',
            'price': 'Null',
            }
        return course             
    else:
        return 0


def udacity_store_course2(item):
    name = item['title']
    url = item['homepage']
    description = "Null"
    course = {}
    course = {
        'name': name,
        'url': url,
        'description': description,
        'provider': 'udacity',
        'price': 'Null',
        }
    return course


def udacity_course(course):
    udacity_courses = []
    url_params = ''
    url = 'https://www.udacity.com/public-api/v0/courses'
    res = requests.get(url)
    results = res.text
    json_result = loads(results)
    for item in json_result['courses']:
        temp = udacity_store_course(item, course)
        if temp:
            udacity_courses.append(temp)
    return udacity_courses


def udacity_all_courses():
    udacity_courses = []
    url_params = ''
    url = 'https://www.udacity.com/public-api/v0/courses'
    res = requests.get(url)
    results = res.text
    json_result = loads(results)
    for item in json_result['courses']:
        temp = udacity_store_course2(item)
        if temp:
            udacity_courses.append(temp)
    return udacity_courses


def udemy_store_course(item):
    name = item['title']
    url = 'https://www.udemy.com' + item['url']
    price = item['price']
    course = {
        'name': name,
        'url': url,
        'price': price,
        'provider': 'udemy',
        'description': 'Null',
        }
    return course


def udemy_course(course):
    udemy_courses = []
    headers = \
        {'Authorization': 'Basic RUFGeGgwblpWQ2RsZndxNUY4VUJpMmZ5WDVPeVYxajBzaHJTd21NMzpJWERvTlVDZlM0Z2xEM3FnekJpZ2FiQjYzM2REdDFua1kwRkY5ejVPb0ZCVnNObkg4ZnRCbmtXWllxR0lzWUlLanF0M2JLM2JSM0xDc2EyWm9zWU5TV3pld2xDNUtzUDVidlNKUDVFMXNaTURIN09nYzZuVkhUMlR0VExYWHJGSw==',
         'Accept': 'application/json, text/plain, */*'}
    url_params = '&is_affiliate_agreed=True&ordering=best_seller'
    url = \
        'https://www.udemy.com/api-2.0/courses/?page_size=100000&search=' \
        + course + url_params
    res = requests.get(url, headers=headers)
    results = res.text
    json_result = loads(results)
    for item in json_result['results']:
        udemy_courses.append(udemy_store_course(item))
    return udemy_courses


def udemy_all_courses(size):
    if not size:
        size = 1000
    udemy_courses = []
    headers = \
        {'Authorization': 'Basic RUFGeGgwblpWQ2RsZndxNUY4VUJpMmZ5WDVPeVYxajBzaHJTd21NMzpJWERvTlVDZlM0Z2xEM3FnekJpZ2FiQjYzM2REdDFua1kwRkY5ejVPb0ZCVnNObkg4ZnRCbmtXWllxR0lzWUlLanF0M2JLM2JSM0xDc2EyWm9zWU5TV3pld2xDNUtzUDVidlNKUDVFMXNaTURIN09nYzZuVkhUMlR0VExYWHJGSw==',
         'Accept': 'application/json, text/plain, */*'}
    url_params = '&is_affiliate_agreed=True&ordering=best_seller'
    url = 'https://www.udemy.com/api-2.0/courses/?page_size=' \
        + str(size) + url_params
    res = requests.get(url, headers=headers)
    results = res.text
    json_result = loads(results)
    for item in json_result['results']:
        udemy_courses.append(udemy_store_course(item))
    return udemy_courses


if __name__ == '__main__':
   
    app.run(debug=True)

			
