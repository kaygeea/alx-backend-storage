-- Create an index on the first letters of entries in a column
CREATE INDEX idx_name_first
          ON names(name(1));
