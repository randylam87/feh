const express = require('express');
const router = express.Router();
const scrape = require('../scrape/scrape.js');

router.get('/', (req, res) => res.send('GET handler for /api route.'));
router.get('/scrape', (req, res) => {
  scrape()
  res.send('Scraping https://fireemblem.gamepress.gg/heroes') 
})


module.exports = router;