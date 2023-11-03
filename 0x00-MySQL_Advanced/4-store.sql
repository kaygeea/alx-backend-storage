-- Create trigger that reduces quantity of an item after a new order is added
DELIMITER $$

CREATE TRIGGER update_item_quantity
  AFTER INSERT
            ON orders
  FOR EACH ROW
	 BEGIN
	       UPDATE items
	          SET quantity = (quantity) - NEW.number
	        WHERE name = NEW.item_name;
	 END$$

DELIMITER ;
