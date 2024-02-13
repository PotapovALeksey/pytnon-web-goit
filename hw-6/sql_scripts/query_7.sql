select groups.name as group_name, subjects.name as subject_name, students.name as student_name, grades.value as grade from students
inner join groups ON groups.id = ?
inner join subjects ON subjects.id = ?
inner join grades ON grades.subject_id = ?
WHERE students.group_id = ?
order by student_name asc
