CREATE TABLE product_record(
            pk CHAR(64) PRIMARY KEY,
            code TEXT NOT NULL,
            type TEXT NOT NULL,
            data TEXT NOT NULL
            );
CREATE INDEX on product_record (code, type);
