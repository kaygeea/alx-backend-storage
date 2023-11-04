-- Create a function that divides 2 numbers and returns their quotient.
-- Args:
--	1. a (int) - incoming argument for the dividend.
--	2. b (int) - incoming argument for the divisor.
-- Returns:
--	The quotient of a & b or 0 if b == 0.
DELIMITER $$

CREATE FUNCTION SafeDiv(a INT, b INT)
        RETURNS FLOAT
  DETERMINISTIC
          BEGIN
		DECLARE quotient FLOAT;

		     IF b = 0
		   THEN
		        SET quotient = 0;
		   ELSE
			SET quotient = a / b;
		    END IF;
		 RETURN (quotient);
          END$$

DELIMITER ;
