cd backend && poetry run beastiary --debug --no-security &
cd frontend && npm run serve &
watchmedo shell-command \
    --patterns="*.py" \
    --recursive \
    --command="bash scripts/kill-running-server.sh && cd backend && poetry run beastiary --debug --no-security &" \
    .
wait
