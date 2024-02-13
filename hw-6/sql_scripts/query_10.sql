select teachers.name as teacher_name, subjects.name as subject_name, students.name as student_name from students
inner join grades on grades.student_id = students.id
inner join teachers on teachers.id = grades.teacher_id
inner join subjects on subjects.teacher_id = teachers.id
where students.id = ? and grades.teacher_id = ?
group by subject_name
