const path = require("path");

module.exports = {
  apps: [
    {
      name: "company-profile",
      cwd: __dirname,
      script: path.join(__dirname, ".venv", "bin", "gunicorn"),
      args: "--bind 127.0.0.1:8765 --workers 2 --timeout 120 app:app",
      interpreter: "none",
      exec_mode: "fork",
      autorestart: true,
      max_restarts: 10,
      restart_delay: 2000,
      time: true,
      env: {
        PYTHONUNBUFFERED: "1",
        HOST: "127.0.0.1",
        PORT: "8765",
        TRUST_PROXY: "1",
      },
    },
  ],
};
