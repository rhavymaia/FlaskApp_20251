DROP TABLE IF EXISTS tb_instituicao;

CREATE TABLE tb_instituicao (
    id SERIAL PRIMARY KEY,
    no_entidade TEXT NOT NULL,
    co_entidade INTEGER NOT NULL,
    qt_mat_bas INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
