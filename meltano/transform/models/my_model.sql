SELECT table_name, column_name, ordinal_position::text AS ordinal_position
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;