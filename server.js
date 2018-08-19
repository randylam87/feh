const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const PORT = process.env.PORT || 8000;
// Routes
const api = require('./server/routes/api.js');

app.listen(PORT, () => console.log(`Server started on: http://localhost:${PORT}`));

// Middleware
app.use(bodyParser.json({type: 'application/vnd.api+json'}));
app.use(bodyParser.urlencoded({extended: false}));
// app.use(express.static(path.resolve(__dirname, 'client', 'build'))); // React Frontend
app.use('/api', api);
