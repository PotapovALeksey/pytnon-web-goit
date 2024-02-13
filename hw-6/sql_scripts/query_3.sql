SELECT groups.name as group_name , subjects.name as subject_name, AVG(grades.value) as avg_grade from grades
INNER JOIN students ON grades.student_id = students.id
INNER JOIN groups ON groups.id = students.group_id
INNER JOIN subjects ON subjects.id = grades.subject_id
WHERE grades.subject_id = ?
GROUP BY group_name
ORDER BY avg_grade DESC
