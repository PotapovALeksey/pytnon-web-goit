SELECT teachers.name as teacher_name, subjects.name as subject_name from subjects
inner join teachers on teachers.id = ?
where subjects.teacher_id = ?
