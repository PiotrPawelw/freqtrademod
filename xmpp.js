const { Client } = require('node-xmpp-client');

const client = new Client({
  jid: 'master@niemazartow.eu',
  password: 'a',
  host: 'niemazartow.eu',
  port: 5223,
  rejectUnauthorized: false // Wyłączenie weryfikacji certyfikatu
});

client.on('online', () => {
  console.log('Connected to XMPP server!');
});
