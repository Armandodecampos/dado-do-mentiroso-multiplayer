-- supabase/migrations/20240726000001_create_sequential_room_function.sql

-- Recria a função para aceitar o creator_id como um parâmetro UUID
CREATE OR REPLACE FUNCTION create_room_with_sequential_code(p_creator_id UUID)
-- Retorna um único registro que corresponde à estrutura da tabela de salas
RETURNS SETOF rooms AS $$
DECLARE
    max_num INT;
    new_code TEXT;
    new_room_id INT;
BEGIN
    -- Repete até que uma sala seja inserida com sucesso
    LOOP
        -- 1. Encontra o maior número de sala existente para evitar colisões
        -- Usa um bloqueio no nível de linha em um registro fictício para serializar as criações de sala
        -- Isso é mais leve do que bloquear a tabela inteira
        PERFORM pg_advisory_xact_lock(1);

        SELECT COALESCE(MAX(CAST(room_code AS INTEGER)), 0)
        INTO max_num
        FROM rooms
        WHERE room_code ~ '^\d+$';

        -- 2. Calcula o novo código da sala
        new_code := (max_num + 1)::text;

        -- 3. Tenta inserir a nova sala
        BEGIN
            INSERT INTO rooms (room_code, creator_id, game_started)
            VALUES (new_code, p_creator_id, false)
            RETURNING id INTO new_room_id;

            -- Se a inserção for bem-sucedida, retorna os dados da nova sala e sai
            RETURN QUERY SELECT * FROM rooms WHERE id = new_room_id;
            EXIT; -- Sai do loop
        EXCEPTION
            -- Se ocorrer uma violação de unicidade (caso raro com o bloqueio),
            -- o loop tentará novamente com um novo número
            WHEN unique_violation THEN
                -- A transação é abortada, o loop tentará novamente na próxima iteração
        END;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
