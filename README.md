# Mock Django Project

Requirement: Make a Django application for to-do list

## Features:

1. User should be able to add his tasks.
2. User should be able to mark task as completed.
3. System should display task relevant to user who logged in.
4. User should be able to view all the task/day.

## Setup:

1. Setup a Django Rest Framework application with browsable API's.
2. Create 5 users in the system for this demo.
3. Select any database of your choice [preferably SQL]
4. System should provide capability to GET, POST, PUT, DELETE a task/user.
5. Define API urls for the app as per features.

## Outcome:

1. Present the deployed solution during interview calls.
2. Explain the flow of applications.
3. Explain challenges faced.
4. Any new learnings/finding which needs highlight.
5. Answer questions as per interview panel

## Endpoints:

### Tasks
| Endpoint       |Method |Description                                                        |
|-----------------|-------|------------------------------------------------------------------|
|/tasks/          |GET	 |Lists Tasks, takes optional parameter 'date' in ISO 8601           |
|/tasks/          |POST  |Create Task                                                        |
|/tasks/\<int:pk\>/|GET	 |Get Task detail                                                    |
|/tasks/\<int:pk\>/|PUT   |Update Task                                                        |
|/tasks/\<int:pk\>/|DELETE|Delete Task                                                        |

Example JSON format:

    { 
	    "due":	"2019-11-21", 
	    "body": 	"Requirement: Make a Django application for to-do list", 
	    "title":	"Complete takehome assignment",
	    "owner": 	"admin",
	    "completed":true
    }


