SELECT student_id, avg(value) as avg_value from grades group by student_id order by avg_value desc limit 5
