-- Create a view to list students who need a meeting
CREATE VIEW need_meeting AS
     SELECT name
       FROM students
      WHERE score < 80.0 AND
            (last_meeting IS NULL
             OR last_meeting > DATE_SUB(CURDATE(), INTERVAL 1 MONTH));
--           OR DATEDIFF(CURDATE(), last_meeting) > 31);
