module.exports = {
  apps: [{
    name: 'raspi-web',
    script: './bin/www',

    instances: 1,
    autorestart: true,
    watch: true,
    ignore_watch: ["node_modules", "storage"],
    env: {
      NODE_ENV: 'development',
      PORT: '3000',
      WS_PORT: '3001'
    },
    env_production: {
      NODE_ENV: 'production',
      PORT: '3000',
      WS_PORT: '3001'
    }
  }]
};