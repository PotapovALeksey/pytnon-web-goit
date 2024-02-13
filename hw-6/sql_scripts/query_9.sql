select students.name as student_name, subjects.name as subject_name from grades
inner join students on students.id = grades.student_id
inner join subjects on subjects.id = grades.subject_id
where student_id = ?
group by subject_name
