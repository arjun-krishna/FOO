var connect = require('connect');
var serveStatic = require('serve-static');
connect().use(serveStatic(__dirname,  {'index': ['index.html']})).listen(3000);