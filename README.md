####### Goal ####### 
Development of a web application called onlineLearner. 

####### Functionalities #######
- A user can see under "My courses" the courses he has created and the ones he is enrolled in. The courses with at least one free place are under "Available courses".
- A user can create courses. Some information about the course (course name, description, total number of places, enrolment key) must be entered in a form and is sent via a mail request.
- Clicking on the title of a course displays the details of the course. The name, the number of free places, the description and a list of exercises of the course are displayed.
- A user can register for existing courses if there is still at least one free place. This can be done after viewing the course details page.
- A user can only delete courses that he has created. If he tries to delete another course, he will receive an error message. Deleting a course is only possible on the course details page.
- On the course details page it is possible to upload a submission for an exercise. A submission contains text. It can only be done once for an exercise.

####### NB: Users are hardcoded for simplicity. Therefore no login functionality. #######



####### Python Installation #######
    1. install Python (https://www.python.org/downloads/) on your computers

####### Change the config parameters #######
    1. replace the values in properties.settings with your account and DB data

####### Create a virtual environment (one-time) #######
    1. navigate to the project folder -> cd ../block3/projekte/python/onlineLearner
    2. python3 -m venv venv
    3. source venv/bin/activate

####### Install the dependencies (once) #######
    pip install -r requirements.txt

####### Starting the web application #######
    From the IDE PyCharm:
        Only the FIRST TIME:
            1. select "Do not import settings".
            2. -> Open -> Online Learner -> Settings -> Project Interpreter -> Add -> venv
            3. under existing environment: select Interpreter ../block3/projekte/python/onlineLearner/venv/bin/python.
               Replace XXX with your group number.

         Otherwise run the script app.py

    From the console:
        1. change to the project directory (e.g. /home/dbpXXX/block3/projects/python/onlineLearner)
        2. activate virtual environment with statement: source venv/bin/activate
        3. Run python app.py

####### To connect to a DB: #######
Revise the properties.settings file.  Use the getExternalConnection() method in DBUtil (in script file connect.py).

Translated with www.DeepL.com/Translator (free version)
