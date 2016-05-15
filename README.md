# pycourses

Pycourses is a MOOC API .

To utilise thi API properly you'll need to follow the syntax mentioned below :-


1  To extract details of a particular course :-

      url:- /course/api/v1.0/courses/course_name

2  To extract details of a particular course from a particular MOOC site :-

      url:- /course/api/v1.0/courses/provider/course_name

      NOTE presently providers are - Coursera,Udemy,Udacity 

3  To extract all courses from coursera :-

      url:- /course/api/v1.0/courses/coursera?start="start results from this number"&limit="number of results to display on a page" 

4  To extract details of all courses from udacity :-

      url:- /course/api/v1.0/courses/udacity

5  To extract details of all courses from udemy :-

      url:- /course/api/v1.0/courses/udemy?pagesize="number of results to display on page"
The API is live at  https://pycourses.herokuapp.com      
