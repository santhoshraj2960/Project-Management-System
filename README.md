
Energylabs **Task Management system (ELTMS)** is a tool designed for creating and managing tasks.

**Screen Shots:**  https://github.com/santhoshraj2960/enerylabs/tree/master/Screen%20Shots%20of%20Project

![Image of social media scheduler](https://github.com/santhoshraj2960/Project-Management-System/blob/master/Screen%20Shots%20of%20Project/Screen%20Shot%202018-07-01%20at%2023.38.39.png)

Requirements
1) Django 1.8
2) Python 2.7

**How to set it up**
1) Download or Clone the git repo on your local system
2) Navigate inside projectmanagement directory
3) Run the following command
   python manage.py migrate
4) Then start the server using the following command
   python manage.py runserver

**How to use Energylabs Task Management**
1) You can create users by going to 
   http://localhost:8000/todolist/registration-page/
2) Create as many users as you want by specifying a unique username and password. The system does not allow 2 users with same username to register. Make sure you are logged out on ELTMS before trying to create a new user.
3) Once you have created the users, Visit 
   http://localhost:8000/todolist/
   and login to any user by specifying appropriate username and password
4) Once logged in, you can create tasks by clicking on Add task button on the top left corner of screen
5) Hide completed tasks button on the top right corner hides the compled tasks and displays only pending tasks
6) To edit/delete/change status of a task click on the task title (which is a link)
7) A task can be edited/deleted/changed status only by:
   7.1) The user for whom the task is assigned to 
   7.2) The user who created the task


The project by default has 1 user signed up with following credentials
1) Username : user1
2) Password : energylabs

This user can be deleted if needed by 
1) Going into projectmanagement directory
2) Run python manage.py shell
3) User.objects.get(username='user1').delete()
