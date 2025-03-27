Set Up:
- Activate virtual environment: source venv/bin/activate
- sqlite3 michigami.db
- Create Tables: .read SQL/create_tables.sql
- Drop Tables: .read SQL/drop_tables.sql
- call loaders: python3 Loaders/filename.py
Run files out Michigami directory

Hiw ti make it run automatically:
./install_cron.sh