CREATE TABLE users
(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  is_admin bool DEFAULT FALSE,
  username string NOT NULL,
  password string NOT NULL
);

CREATE TABLE products
(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title string NOT NULL,
  price double NOT NULL,
  description string NOT NULL,
  image string NOT NULL
);

CREATE TABLE orders
(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id INTEGER NOT NULL,
  quantity double NOT NULL,
  total double NOT NULL,
  FOREIGN KEY(product_id) REFERENCES products(id)
);

CREATE TABLE comments
(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id INTEGER NOT NULL,
  message string NOT NULL,
  FOREIGN KEY(product_id) REFERENCES products(id)
)