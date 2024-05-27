
******Materials and solution*************

-Materials:

- Two folders are delivered:

	- docker-spark-cluster-master -> 
	
		- Docker solution, with own spark clusters (master and worker) defined in docker-compose
		- Dockerfile performs needed installations
		- The entry point is defined in stark-spark.sh file as the python module in /apps/main.py
		- apps/main.py includes the main source pyspark code
		- main_test.py(in test folder) includes the main testing module
	
		
	- jupyter-notebook -> 
	
	a jupyter notebook with description of data processing and code used during testing
	
- Solution

This solution uses pyspark batch and structured streaming to perform the needed tasks.

Task 1: Read file as batch

 - The program starts a Spark session 
 - It then reads the file from the URL and copy the information to a dataframe (raw_df)
 - Rename columns and apply needed transformations to cleand the data from \N values
 - Using spark.sql it selects the top 10 airports as source from the new dataframe (df_new)
 - It writes the output the ./data/output/batch as csv file
 
Task 2: Read Stream

 - the stream is read and the schema is defined
 - apply transformations to streaming dataframe, adding a dummy_timestamp to perform windowing
 - streaming dataframe schema is printed and output is writen to console (using writeStream)
 

Task 3: Use sliding windows

- using the streaming dataframe, the program selects 10 minutes windows every 5 minutes using window() function
- print output to console

Task 4: Adding unit test

- This part is added in test_main.py, using unittest module. Added for reference.


******Running solution*************

docker-spark-cluster-master

Requirements:

- docker*
- docker-compose

*the docker engine should be up and running

From the docker-spark-cluster-master folder, open a terminal and run the following commands:


Building the image -> docker build -t cluster-apache-spark:3.0.2 .
Run the docker compose -> docker-compose up -d

This should create the container and images needed for the spark cluster
You can validate the cluster from the UI URL http://localhost:9090/

Now connect to the master or worker cluster and run the app:


/opt/spark/bin/spark-submit --master spark://spark-master:7077 \
--driver-memory 1G \
--executor-memory 1G \
/opt/spark-apps/main.py


You shoulds see now that the job is running.
The ouput file from the batch job is saved in /app/files container directory with a part-XXXX-xxx.csv name (spark does not allow to name it)


To run the notebook, you can use jupyter (jupyter notebook from conda terminal or can be also open with VSCode)

The notebook includes the processing steps and can be a good quick overview of the solution (without testing modules).


*Please mind that error handling (try/catch) is not implemented in the code as it should in production environment.

Please also note that,

as per time and system limitations, the solution has only been tested in docker desktop on windows 11 machine.
Even though it's not a perfect working solution (windowing part is more pseudocode than code itself, as the streaming part),
I think it can give you an idea of my current knowledge, being the case I haven't used this techs in my current or past roles.
The logic of the testing module is also implemented in /test folder, althought not included along with main for simplicity.
I didn't want to spend much time on it as suggested, to give you an honest image of my current skillset in these matters.
Learning on the go has been so nice! and I will love to further discuss the solution it with you.