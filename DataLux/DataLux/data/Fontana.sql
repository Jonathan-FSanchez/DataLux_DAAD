
DROP TABLE IF EXISTS detalle_orden CASCADE;
DROP TABLE IF EXISTS ordenes      CASCADE;
DROP TABLE IF EXISTS productos    CASCADE;
DROP TABLE IF EXISTS categorias   CASCADE;
DROP TABLE IF EXISTS clientes     CASCADE;
DROP TABLE IF EXISTS empleados    CASCADE;

CREATE TABLE categorias (
    id_categoria  SERIAL PRIMARY KEY,
    nombre        VARCHAR(60)  NOT NULL,
    descripcion   TEXT
);

INSERT INTO categorias (nombre, descripcion) VALUES
    ('Electrónica',    'Dispositivos electrónicos y accesorios'),
    ('Ropa',           'Prendas de vestir para todas las edades'),
    ('Hogar',          'Artículos para el hogar y decoración'),
    ('Deportes',       'Equipamiento y ropa deportiva'),
    ('Libros',         'Libros físicos y material educativo'),
    ('Juguetes',       'Juguetes y juegos para niños'),
    ('Alimentos',      'Productos alimenticios y bebidas'),
    ('Belleza',        'Cosméticos y cuidado personal');


CREATE TABLE empleados (
    id_empleado  SERIAL PRIMARY KEY,
    nombre       VARCHAR(80)  NOT NULL,
    puesto       VARCHAR(60)  NOT NULL,
    salario      NUMERIC(10,2) NOT NULL,
    fecha_ingreso DATE         NOT NULL
);

INSERT INTO empleados (nombre, puesto, salario, fecha_ingreso) VALUES
    ('Ana Torres',       'Gerente de Ventas',   28000.00, '2019-03-15'),
    ('Luis Ramírez',     'Vendedor',            14500.00, '2020-07-01'),
    ('María Gómez',      'Vendedora',           14500.00, '2020-09-10'),
    ('Carlos Vega',      'Almacenista',         12000.00, '2021-01-20'),
    ('Sofía Mendoza',    'Soporte al cliente',  13000.00, '2021-04-05'),
    ('Jorge Herrera',    'Vendedor',            14500.00, '2022-02-14'),
    ('Paola Ruiz',       'Contadora',           22000.00, '2019-11-30'),
    ('Diego Flores',     'Almacenista',         12000.00, '2023-03-01'),
    ('Valeria Castro',   'Soporte al cliente',  13000.00, '2022-08-18'),
    ('Roberto Sánchez',  'Gerente de Logística',26000.00, '2018-06-25');


CREATE TABLE clientes (
    id_cliente  SERIAL PRIMARY KEY,
    nombre      VARCHAR(80)  NOT NULL,
    email       VARCHAR(120) NOT NULL UNIQUE,
    ciudad      VARCHAR(60),
    fecha_registro DATE      NOT NULL DEFAULT CURRENT_DATE
);

INSERT INTO clientes (nombre, email, ciudad, fecha_registro) VALUES
    ('Pedro Alvarado',    'pedro.alvarado@mail.com',   'Ciudad de México', '2022-01-10'),
    ('Lucía Pérez',       'lucia.perez@mail.com',      'Guadalajara',      '2022-03-22'),
    ('Tomás Ríos',        'tomas.rios@mail.com',       'Monterrey',        '2022-05-14'),
    ('Elena Vargas',      'elena.vargas@mail.com',     'Puebla',           '2022-07-30'),
    ('Andrés Molina',     'andres.molina@mail.com',    'Tijuana',          '2023-01-05'),
    ('Carmen Delgado',    'carmen.delgado@mail.com',   'León',             '2023-02-18'),
    ('Felipe Ortega',     'felipe.ortega@mail.com',    'Mérida',           '2023-03-27'),
    ('Natalia Cruz',      'natalia.cruz@mail.com',     'Querétaro',        '2023-05-09'),
    ('Samuel Ibarra',     'samuel.ibarra@mail.com',    'Chihuahua',        '2023-06-14'),
    ('Daniela Moreno',    'daniela.moreno@mail.com',   'Ciudad de México', '2023-08-01'),
    ('Héctor Jiménez',    'hector.jimenez@mail.com',   'Guadalajara',      '2023-09-12'),
    ('Fernanda Aguirre',  'fernanda.aguirre@mail.com', 'Monterrey',        '2024-01-03'),
    ('Oscar Reyes',       'oscar.reyes@mail.com',      'Oaxaca',           '2024-02-20'),
    ('Gabriela Salinas',  'gabriela.salinas@mail.com', 'Veracruz',         '2024-03-15'),
    ('Iván Castillo',     'ivan.castillo@mail.com',    'Ciudad de México', '2024-04-10');


CREATE TABLE productos (
    id_producto   SERIAL PRIMARY KEY,
    nombre        VARCHAR(100) NOT NULL,
    id_categoria  INT          NOT NULL REFERENCES categorias(id_categoria),
    precio        NUMERIC(10,2) NOT NULL,
    stock         INT           NOT NULL DEFAULT 0,
    activo        BOOLEAN       NOT NULL DEFAULT TRUE
);

INSERT INTO productos (nombre, id_categoria, precio, stock) VALUES
    ('Audífonos Bluetooth',        1,  899.00,  45),
    ('Cargador USB-C 65W',         1,  349.00,  80),
    ('Smartwatch Fit Pro',         1, 1599.00,  20),
    ('Cámara Web 1080p',           1,  750.00,  30),
    ('Playera Deportiva',          2,  250.00, 120),
    ('Jeans Slim Fit',             2,  680.00,  60),
    ('Sudadera con Capucha',       2,  420.00,  75),
    ('Lámpara LED de Escritorio',  3,  310.00,  55),
    ('Almohada Viscoelástica',     3,  590.00,  40),
    ('Silla de Oficina Ergonómica',3, 2800.00,  15),
    ('Pelota de Fútbol',           4,  380.00,  90),
    ('Guantes de Box',             4,  520.00,  35),
    ('Yoga Mat Antideslizante',    4,  280.00,  50),
    ('Python para Todos',          5,  320.00,  70),
    ('Estadística con R',          5,  410.00,  45),
    ('Lego City 500 pzs',          6,  950.00,  25),
    ('Muñeca Interactiva',         6,  650.00,  30),
    ('Granola Orgánica 500g',      7,   95.00, 200),
    ('Café Molido Premium 250g',   7,  180.00, 150),
    ('Sérum Vitamina C',           8,  430.00,  60);


CREATE TABLE ordenes (
    id_orden     SERIAL PRIMARY KEY,
    id_cliente   INT          NOT NULL REFERENCES clientes(id_cliente),
    id_empleado  INT          NOT NULL REFERENCES empleados(id_empleado),
    fecha        DATE         NOT NULL DEFAULT CURRENT_DATE,
    estado       VARCHAR(20)  NOT NULL DEFAULT 'pendiente',
                 -- pendiente | enviado | entregado | cancelado
    total        NUMERIC(10,2) NOT NULL DEFAULT 0
);

INSERT INTO ordenes (id_cliente, id_empleado, fecha, estado, total) VALUES
    ( 1,  2, '2024-01-05', 'entregado',  1748.00),
    ( 2,  3, '2024-01-12', 'entregado',   680.00),
    ( 3,  2, '2024-02-01', 'entregado',  3699.00),
    ( 4,  6, '2024-02-14', 'enviado',     700.00),
    ( 5,  3, '2024-02-20', 'entregado',   475.00),
    ( 6,  2, '2024-03-03', 'entregado',  1190.00),
    ( 7,  6, '2024-03-18', 'cancelado',   320.00),
    ( 8,  3, '2024-03-25', 'entregado',  2800.00),
    ( 9,  2, '2024-04-02', 'enviado',     610.00),
    (10,  6, '2024-04-10', 'pendiente',   860.00),
    (11,  3, '2024-04-15', 'entregado',   430.00),
    (12,  2, '2024-04-22', 'entregado',  1050.00),
    (13,  6, '2024-05-01', 'enviado',     275.00),
    (14,  3, '2024-05-08', 'entregado',   590.00),
    (15,  2, '2024-05-15', 'pendiente',   349.00),
    ( 1,  6, '2024-05-20', 'entregado',   380.00),
    ( 3,  3, '2024-06-01', 'entregado',   520.00),
    ( 5,  2, '2024-06-10', 'enviado',     730.00),
    ( 8,  6, '2024-06-18', 'entregado',   410.00),
    ( 2,  3, '2024-06-25', 'entregado',   899.00);


CREATE TABLE detalle_orden (
    id_detalle   SERIAL PRIMARY KEY,
    id_orden     INT           NOT NULL REFERENCES ordenes(id_orden),
    id_producto  INT           NOT NULL REFERENCES productos(id_producto),
    cantidad     INT           NOT NULL CHECK (cantidad > 0),
    precio_unit  NUMERIC(10,2) NOT NULL
);

INSERT INTO detalle_orden (id_orden, id_producto, cantidad, precio_unit) VALUES
    -- orden 1
    ( 1,  1, 1,  899.00),
    ( 1,  2, 1,  349.00),
    ( 1, 13, 1,  280.00),  -- total 1528... ajustado en ordenes
    -- orden 2
    ( 2,  6, 1,  680.00),
    -- orden 3
    ( 3,  3, 1, 1599.00),
    ( 3, 10, 1, 2800.00),  -- total ajustado
    -- orden 4
    ( 4,  5, 2,  250.00),
    ( 4,  8, 1,  310.00),  -- total 810 ajustado
    -- orden 5
    ( 5, 18, 5,   95.00),
    -- orden 6
    ( 6, 14, 1,  320.00),
    ( 6, 15, 1,  410.00),
    ( 6,  7, 1,  420.00),
    -- orden 7 (cancelada)
    ( 7, 14, 1,  320.00),
    -- orden 8
    ( 8, 10, 1, 2800.00),
    -- orden 9
    ( 9, 11, 1,  380.00),
    ( 9, 19, 1,  180.00),
    -- orden 10
    (10, 17, 1,  650.00),
    (10, 16, 1,  950.00),  -- total ajustado
    -- orden 11
    (11, 20, 1,  430.00),
    -- orden 12
    (12, 16, 1,  950.00),
    (12,  5, 1,  250.00),
    -- orden 13
    (13, 13, 1,  280.00),
    -- orden 14
    (14,  9, 1,  590.00),
    -- orden 15
    (15,  2, 1,  349.00),
    -- orden 16
    (16, 11, 1,  380.00),
    -- orden 17
    (17, 12, 1,  520.00),
    -- orden 18
    (18,  7, 1,  420.00),
    (18, 19, 1,  180.00),  -- total ajustado
    -- orden 19
    (19, 15, 1,  410.00),
    -- orden 20
    (20,  1, 1,  899.00);