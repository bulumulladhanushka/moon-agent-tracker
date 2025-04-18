#!/bin/sh

if [ "$RUN_MODE" = "server" ]; then
    echo "[RUN_MODE=server] Starting Flask API server..."
    python app.py
else
    echo "[RUN_MODE=job] Running CronJob aggregation tasks..."
    python app.py
fi
