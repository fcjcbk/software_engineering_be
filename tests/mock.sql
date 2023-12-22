use OJ;
/* student
{
  "userid": 123,
  "username": "student",
  "password": "$2b$12$XxOFcfyZbMlhgv0kmkef1OjlhC8CWhm/aAW0MBnkLzNQxXMeykjhK",
  "email": "123@qq.com",
  "role": 0,
  "telephone": "string",
  "major": "string"
} */
INSERT INTO user VALUES(123,  '123@qq.com', 'student', '$2b$12$XxOFcfyZbMlhgv0kmkef1OjlhC8CWhm/aAW0MBnkLzNQxXMeykjhK', 0, 'string', 'string');

/* teacher
{
  "userid": 1234,
  "username": "teacher",
  "password": "$2b$12$LSEV/rZCRFu7efPy3c6/b.zpcYGbCpFKKEoIfdewvxznefVQ6cvKm",
  "email": "1234@qq.com",
  "role": 1,
  "telephone": "string",
  "major": "string"
} */

INSERT INTO user VALUES(1234,  '1234@qq.com', 'teacher', '$2b$12$LSEV/rZCRFu7efPy3c6/b.zpcYGbCpFKKEoIfdewvxznefVQ6cvKm', 1, 'string', 'string');

/* courser
{
  "courseid": 0,
  "name": "course",
  "info": "string",
  "teacherid": 1234
} */

INSERT INTO course VALUES(0, 'course', 'string', 1234);

/* homeowrk
{
  "homeworkid": 0,
  "homeworkname": "homework",
  "duedate": "2023-12-22T13:57:25.999Z",
  "courseid": 0
} */

INSERT INTO homework VALUES(0, 'homework', '2023-12-22 13:57:25.999', 0);

insert into problem values(0, "problem", "blank", "problem-content", 10, 0, "hard");

/* {
  "solutionid": 0,
  "name": "solution",
  "content": "content of solution",
  "problemid": 0,
  "contributorid": 123
} */

INSERT INTO solution value(0,  "content of solution", 0, 123, "solution");