CREATE TABLE IF NOT EXISTS pacientes (
    paciente_id INT,
    nombre VARCHAR (50),
    PRIMARY KEY (paciente_id)
);

COPY pacientes(paciente_id,nombre)
FROM 'C:\Users\charl\Documents\Nutricion\pacientes.csv'
DELIMITER ','
CSV HEADER;

CREATE TABLE IF NOT EXISTS visitas (
    visita_id INT,
    paciente_id INT,
    fecha DATE,
    PRIMARY KEY (visita_id),
    FOREIGN KEY (paciente_id) REFERENCES pacientes(paciente_id)
);

COPY visitas(visita_id, paciente_id, fecha)
FROM 'C:\Users\charl\Documents\Nutricion\visitas.csv'
DELIMITER ','
CSV HEADER;

CREATE TABLE IF NOT EXISTS mediciones (
    medida_id INT,
    visita_id INT,
    paciente_id INT,
    medida VARCHAR (40),
    valor FLOAT,
    PRIMARY KEY (medida_id),
    FOREIGN KEY (visita_id) REFERENCES visitas(visita_id),
    FOREIGN KEY (paciente_id) REFERENCES pacientes(paciente_id)
);

-- COPY mediciones(medida_id, visita_id, paciente_id, medida, valor)
-- FROM 'C:\Users\charl\Documents\Nutricion\mediciones.csv'
-- DELIMITER ','
-- CSV HEADER;

-- DROP VIEW karen;
-- CREATE OR REPLACE VIEW karen AS
-- SELECT nombre,fecha,medida_id,medida,valor FROM
--     (SELECT nombre, visita_id, medida_id, medida, valor 
--     FROM mediciones LEFT JOIN pacientes 
--     ON mediciones.paciente_id = pacientes.paciente_id) AS k JOIN
-- visitas ON k.visita_id = visitas.visita_id;

SELECT nombre,fecha,medida_id,medida,valor 
FROM karen ORDER BY nombre, fecha, medida;


