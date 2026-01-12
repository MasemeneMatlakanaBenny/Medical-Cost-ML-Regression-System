# ML SYSTEM FOR REGRESSION PROBLEM

This is a machine learning system designed for a regression medical cost problem.We predict the annual medical cost of clients based on their historical available data including transictions.

At first we extract the data,transform it and load it into the lakehouse .
Throughout each phase of data extraction,data quality checks are performed using great_expectations to ensure that we collected and are working with the correct data before machine learning 
comes into play. 

From there,we develop the models using the data we extracted and transformed in order to make future predictions. However since the aim is to develop a machine learning system ,in this case,we are working on a batch machine learning system. It should be noted that a batch machine learning system is the type of machine learning system in which we make predictions offline. This means that there might be no need to include online hosting using FastAPI to send predictions to the users but in a case where such should be made,Kafka plays a huge role.

Back to the system, model quality checks are performed in the same manner as data quality checks but with more consideration and focus on model metrics now.
Drift detection and feature selection are also performed with the use of deepchecks and a mathematical formulae developed with the use of statistical modeling rather than using built-in scikit-learn methods. Models ,metrics,data quality and model quality checks results are all saved in certain respective folders for proper structure of the distributed system.

Tools and libraries used in the workflow can be found in the requirements.txt file.


----

## Setup and Virtual Environment:

The first step before running any code or creating any files is creating a vritual environment to install these dependencies that will be used to accomplish the system. 
Using Windows,the following command on a Powershell terminal in vscode can be used to create the virtual environment:

python -m venv med_env

med_env is the name of the virtual environment ,it should be noted that one can name it as they like.

Then to activate the environment:

.\med_env\Scripts\Activate.ps1 

replacing med_env with the name of the virtual environment created

----

## ETL Workflow:

-- In the ETL workflow ,we are concerned with getting our hands on the dataset first.  The dataset is extracted from the database with the use of SQLAlchemy ,transformed with the use of pandas and loaded into the hopsworks lakehouse for future analytics and consumption. As explained in the each ETL phase,data quality checks are performed to ensure clean ,reliable ,consistent and accurate data before further 
work with it.


