SELECT subjects.name as subject_name, students.name as student_name, avg(value) as avg_value from grades
inner join students ON students.id = student_id
inner join subjects ON subjects.id = ?
where subject_id = ? group by student_id order by avg_value desc
