***My idea***

Create a Django API with the rest_framework template that reads the API info from a postgresql database.
It would be more convenient to run the database in a docker container to avoid some of the followint steps. 
Please see the notes section below for further details.


***Requirements**

Python
PostgresSQL
pgAdming (optional to create database)
Postman (or web browser) to send GET request


***How to Run (on windows)***

- The first step is to create postgresSQL server with following details(for example using pgAdmin):

	Name: django-test-server
	Connection:
		Host name/address: localhost
		Port: 5432
		username:postgres
		password:<the_root_user_pass_of_your_postgresql>
		
	Please create also a database in that server with name
	
		djago_test_db

- Go to DjangoApp/DjangoAPI and edit .env file with your password and save it.

- This runs in a python virtual env. Open a terminal in DjangoAPP folder and run

>Scripts\activate

- Now run >python manage.py makemigrations SessionsApp

- Now run >python manage.py migrate SessionsApp

This will migrate the models to the database. It may display some warnings.

- Now you can run the API by typing >python manage.py runserver

This will display some log information and start the API service,
wait a few seconds until the terminal shows the localhost URL 
where we can send our requests.

- To send a request, open a browser (I recommend using Postman) and send a GET request to <yourlocalhost>/metrics/orders (usually http://127.0.0.1:8000/metrics/orders)
You can retrieve the host from the terminal window while running. Only GET requests are allowed.

- This should return the results (customer_id,median_visits_before_order,median_session_duration_minutes_before_order) in JSON format.
Please note the results are not correct at this moment since the Sessionalization and SQL scripts should be refined.


****Notes****

As mentioned above, probably a more convenient way is to create the database in a docker container as suggested in the assesment. 
Unfortunately I run over some issues with the docker engine start and had not full control over the machine to activate virtualization at BIOS level.
This could be achive by creating a docker-compose file within the project. This also allows to integrate the SQL scripts into a .sql file that can run at startup.
Please also note as mentioned above that the results at this moment are not correct since the SQL is not fully correct, I did not want to spent more time that suggested to give you a realistic image of my current skillset, being the case I haven't used this technologies in my current role. It was really nice and challenging and I would love to 
further discuss the solution with you.

Please also note the idea was to include everything in a virtual environment to avoid module errors, but it has only been tested on windows.
Please check the requirements.txt file for further information.





