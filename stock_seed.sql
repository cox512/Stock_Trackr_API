DROP TABLE stock IF EXISTS;
CREATE TABLE IF NOT EXISTS stock;
INSERT INTO stock (company_name, ticker, current_price, open_price, close_price, day_high, day_low, volume, created_at) VALUES ('Apple Inc.', 'AAPL', 457.10, 453.74, 455.61, 458.01, 453.74,'50600000', date('now'));