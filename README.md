# Log Analyser

## Objective

Summary - This project mainly entails developing a Python script with the following scope:

1.1 Parse auth.log: Extract command usage, with timestamp, executing user and command.
1.2 Parse auth.log: Monitor user authentication changes. 

Print details of newly added users, including the Timestamp. 
Print details of deleted users, including the Timestamp. 
Print details of changing passwords, including the Timestamp. 
Print details of when users used the su command. 
Print details of users who used the sudo; include the command. 
Print ALERT! If users failed to use the sudo command; include the command. 

Aim - This project aims to primarily test student’s Python scripting knowledge, as well as to build up knowledge and familiarity with critical log files such as auth.log. Beyond the format of the file itself, the aim is also to sensitise students to important information and approaches that may be required when processing and analysing logs. 

### Tools Used

- Python
