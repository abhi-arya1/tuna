source venv/bin/activate 
python run.py &
echo "Server started successfully."
cd browser
bun run dev & 
echo "Browser started successfully."