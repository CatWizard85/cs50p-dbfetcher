-- articoli
CREATE TABLE articoli (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codart TEXT UNIQUE NOT NULL, -- Wincorum article id
    codice TEXT,
    spessore REAL,
    scelta REAL,
    grammi REAL,
    lato_a REAL,
    lato_b REAL,
    descrizione TEXT,
    um TEXT,
    giacenza REAL DEFAULT 0,
    ubicazione TEXT,
    fsc_1 TEXT,
    fsc_2 TEXT,
    gest_lotti BOOLEAN DEFAULT 0,
    note TEXT
);

-- clienti
CREATE TABLE clienti (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cod_clie TEXT UNIQUE NOT NULL, -- Wincorum client id
    nome TEXT NOT NULL,
    indirizzo TEXT,
    citta TEXT,
    provincia TEXT,
    num_tel TEXT,
    note TEXT
);

-- fornitori
CREATE TABLE fornitori (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cod_forn TEXT UNIQUE NOT NULL, -- Wincorum supplier id
    nome TEXT NOT NULL,
    indirizzo TEXT,
    citta TEXT,
    provincia TEXT,
    num_tel TEXT,
    note TEXT
);

-- movimenti
CREATE TABLE movimenti (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    record INTEGER NOT NULL, -- Wincorum transaction id
    tipo_mov TEXT NOT NULL CHECK (tipo_mov IN ('carico', 'scarico')),
    data TEXT NOT NULL,  -- use TEXT ISO8601 for dates
    tipo_doc TEXT NOT NULL CHECK (tipo_doc IN ('giac_iniziale', 'ddt_carico', 'ddt_scarico', 'int_carico', 'int_scarico')),
    num_doc INTEGER,
    cod_forn TEXT,
    cod_clie TEXT,
    codart TEXT,
    cod_lotto TEXT,
    descrizione TEXT,
    um TEXT,
    quantita REAL NOT NULL,
    prezzo REAL,
    note TEXT,
    FOREIGN KEY (codart) REFERENCES articoli (codart),
    FOREIGN KEY (cod_clie) REFERENCES clienti (cod_clie),
    FOREIGN KEY (cod_forn) REFERENCES fornitori (cod_forn)
);

-- lotti
CREATE TABLE lotti (
    codart TEXT NOT NULL,
    cod_lotto TEXT NOT NULL,
    giacenza REAL,
    note TEXT,
    PRIMARY KEY (codart, cod_lotto),
    FOREIGN KEY (codart) REFERENCES articoli (codart)
);
