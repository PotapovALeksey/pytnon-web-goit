select teachers.name as teacher_name, subjects.name as subject_name, avg(grades.value) as avg_grade from teachers
inner join grades on grades.teacher_id = teachers.id
inner join subjects on subjects.teacher_id = teachers.id
where teachers.id = ?
group by subject_name
