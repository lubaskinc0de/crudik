-- Сreating user for grafana
CREATE USER grafana WITH PASSWORD 'grafana-password';

GRANT CONNECT ON DATABASE postgres TO grafana;
GRANT USAGE ON SCHEMA public TO grafana;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO grafana;

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO grafana;

-- Сreating user for migrations
CREATE USER migrations WITH PASSWORD 'migrations-password';

GRANT CONNECT ON DATABASE postgres TO migrations;
GRANT CREATE, USAGE ON SCHEMA public TO migrations;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO migrations;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO migrations;

-- Сreating app user
CREATE USER app_user WITH PASSWORD 'app-password';

GRANT CONNECT ON DATABASE postgres TO app_user;
GRANT USAGE ON SCHEMA public TO app_user;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO app_user;

-- Grant permissions on future tables created by migrations user
ALTER DEFAULT PRIVILEGES FOR ROLE migrations IN SCHEMA public 
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_user;

ALTER DEFAULT PRIVILEGES FOR ROLE migrations IN SCHEMA public 
    GRANT USAGE ON SEQUENCES TO app_user;