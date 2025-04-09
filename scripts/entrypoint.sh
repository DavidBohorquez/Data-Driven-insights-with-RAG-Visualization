#!/bin/sh
if [ ! -f /data/publications.db ]; then
    echo "Creating database..."
    sqlite3 /data/publications.db < /scripts/init.sql
    echo "Database created successfully"
fi

# Step 1: Convert data to Hugging Face format
#echo "Converting data to Hugging Face format..."
#python /app/convert_to_hf.py

# Step 2: Fine-tune the model using the generated dataset
#echo "Fine-tuning model..."
#python ./sql_fine_tuning.py
#echo "Fine-tuning completed successfully"

# Step 3: Execute the SQL code generation
#echo "Running SQL code generation..."
#python ./sqlcoder.py

# Unit Tests and Integration Tests
#echo "Running unit tests..."
#python -m pytest ./tests/test_sqlcoder.py -v

# Keep the container running
#exec tail -f /dev/null
exec "$@"