USE students_sql;
CREATE TABLE if NOT EXISTS students  (
    students_id INT PRIMARY KEY,
    name VARCHAR(100),
    height DECIMAL(5,2)
);

insert ignore into students (students_id, name, height) values (1, 'John Doe', 150.9);
insert ignore into students (students_id, name, height) values (2, 'Jane Smith', 160.5);
insert ignore into students (students_id, name, height) values (3, 'Alice Johnson', 155.2);
select * from students;

update students set height = 165.0 where students_id = 2;
update students set name = 'ligoudan' where students_id = 3;
select * from students;

delete from students where students_id = 1;
select * from students;