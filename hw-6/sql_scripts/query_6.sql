SELECT groups.name as group_name, students.name as student_name from students
inner join groups ON groups.id = ?
where students.group_id = ?
