## Fastest Finger First 

[![pipeline status](https://gitlab.com/ramitsurana/fastest-finger-first/badges/master/pipeline.svg)](https://gitlab.com/ramitsurana/fastest-finger-first/commits/master)

Quick quiz based on Serverless

## Features

* Automatic sorting of game scores based on time and score
* Starting from Last Question attempted in case of Logout
* Time out sessions for each question.
* Verification of answers enabled using AWS Lambda Function. 
* Synchronized starting time for each player
* Capacity upto 100 players playing together at a single instance of time.

## Architecture

![fastest-finger-first](https://user-images.githubusercontent.com/8342133/31328546-6f49ea64-acf3-11e7-9408-b066368cb979.png)

## Frontend

It is based on HTML, CSS and Javascript. The questions have a 20 sec window timer after which the next question loads automatically.

## Backend

The entire backend is built on serverless technology: AWS Lambda. It has three lambda functions:
1. registration_check (register.py): Ensures that any registered user can resume from his last session. New users start afresh.
2. update_db (update_rds.py): Each time an answer is submitted, this lambda function updates the DB. 
3. build_leadership_borad (app.py): Uploads a JSON sorted file to s3 bucket. 'app.py' is the python code.
4. get_individual_score (get_score.py): Gets the individual score (number of correct answers and the total time consumed) of a user at the end of the quiz. 

The application uses two tables: 
1. registration_info: Stores the last attempted question details of a user. It has three columns - Phone Number (Primary Key), User Name, QuestionNumber. A sample table would like this:

|   PhoneNumber  |  UserName  | QuestionNumber |
|----------------|:----------:|---------------:|
|   9999999999   |  Srushith  |       5        |
|   8888888888   |  Ramit     |       8        |
|   7777777777   |  Ashvini   |       7        |


2. user_data: Stores the user data like Phone Number (Primary Key), User Name, Question Number, Answer, Time Taken (in seconds). A sample table would like this:


|  PhoneNumber   |  UserName  | QuestionNumber | Answer | TimeTaken (s) |
|----------------|:----------:|---------------:|-------:|--------------:|
|   9999999999   |  Srushith  |       5        |   4    |      15       |
|   8888888888   |  Ramit     |       8        |   2    |       8       |
|   7777777777   |  Ashvini   |       7        |   1    |      11       |


The quiz starts from the register page (index.html). Here the players can fill out there information such as Name and Phone No.

<div align="center"><img src ="https://user-images.githubusercontent.com/23396903/31439175-deaa76d8-aea8-11e7-811a-527b9f5e4d29.PNG" /></div>
<div align="center"><p>Fig 1: Registration page</p></div>

When a user clicks on the 'Register' button, registration_check lambda is called that checks the registration_info table for any previous entries on the same phone number. If found, returns the value of QuestionNumber for that PhoneNumber and if not returns a zero (0). 
Upon recieving a non-zero value, the 'value+1' question would be displayed, resuming the previous session. If a zero is recieved, the quiz starts from the beginning. 

<div align="center"><img src ="https://user-images.githubusercontent.com/23396903/31440343-346b6f1a-aead-11e7-910f-17a41e9cb09e.PNG" /></div>
<div align="center"><p>Fig 2: Question Page</p></div>


Figure 2 shows a sample questions page where a user can select an of the four options and click on submit for submiting the answer. When a user clicks on the 'Submit' button, the update_db lambda function is called with 'Phone Number', 'User Name', 'Question', 'Answer', 'Time' as the parameters. This lambda function verfies for the answer and updates 

Here the verification step for the game happens.Only when the answer is correct, an entry is made for the user in the database along with Time, Question No. and Name of the player.

### RDS Setup

For our use case we have taken MySql as the database on RDS (Relational Database). You can check out more info [here](http://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_MySQL.html). 

**Note:** In case of any security issues, please make sure to check the security groups allocated with the RDS Database.

### S3

It consists of the following steps:

1. Create a S3 bucket.
2. Put an empty json file in the S3 bucket.
3. Make sure to make the file public by changing the permissions of read and write for the file.

**Note:** Remember to enable CORS configuration for the S3 bucket. Refer to this <a href "http://docs.aws.amazon.com/AmazonS3/latest/user-guide/add-cors-configuration.html">post</a> for the instructions. 

## License

MIT License
