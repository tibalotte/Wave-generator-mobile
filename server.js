#!/usr/bin/env node
/*
 * Petit serveur HTTP sans dépendance pour diffuser le Wave Generator
 * sur le réseau local.
 *
 * Point clé : on écoute sur 0.0.0.0 (toutes les interfaces) et non sur
 * 127.0.0.1 / localhost, sinon les autres ordinateurs du réseau ne peuvent
 * pas se connecter.
 *
 * Utilisation :
 *   node server.js            (port 8080 par défaut)
 *   PORT=3000 node server.js  (autre port)
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');

const PORT = parseInt(process.env.PORT, 10) || 8080;
const HOST = '0.0.0.0'; // écoute sur toutes les interfaces réseau
const ROOT = __dirname;

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
};

const server = http.createServer((req, res) => {
  // On ne garde que le chemin, sans query string, et on empêche le
  // "path traversal" (../).
  let urlPath = decodeURIComponent(req.url.split('?')[0]);
  if (urlPath === '/') urlPath = '/index.html';

  const filePath = path.join(ROOT, path.normalize(urlPath));
  if (!filePath.startsWith(ROOT)) {
    res.writeHead(403);
    res.end('403 Forbidden');
    return;
  }

  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end('404 Not Found');
      return;
    }
    const ext = path.extname(filePath).toLowerCase();
    res.writeHead(200, { 'Content-Type': MIME[ext] || 'application/octet-stream' });
    res.end(data);
  });
});

// Liste les adresses IPv4 locales (192.168.x.x, 10.x.x.x, etc.)
function localAddresses() {
  const nets = os.networkInterfaces();
  const addrs = [];
  for (const name of Object.keys(nets)) {
    for (const net of nets[name] || []) {
      if (net.family === 'IPv4' && !net.internal) {
        addrs.push(net.address);
      }
    }
  }
  return addrs;
}

server.listen(PORT, HOST, () => {
  console.log('\n  Wave Generator — serveur réseau local démarré\n');
  console.log(`  Sur cet ordinateur :   http://localhost:${PORT}`);
  const addrs = localAddresses();
  if (addrs.length) {
    console.log('\n  Depuis un autre appareil du réseau, ouvre :');
    for (const a of addrs) {
      console.log(`     http://${a}:${PORT}`);
    }
  } else {
    console.log('\n  (Aucune adresse réseau locale détectée — es-tu connecté au Wi-Fi/Ethernet ?)');
  }
  console.log('\n  Si un autre appareil n\'y arrive pas : vérifie le pare-feu (voir README.md).');
  console.log('  Ctrl+C pour arrêter.\n');
});

server.on('error', (err) => {
  if (err.code === 'EADDRINUSE') {
    console.error(`\n  Le port ${PORT} est déjà utilisé. Essaie : PORT=8081 node server.js\n`);
  } else {
    console.error(err);
  }
  process.exit(1);
});
