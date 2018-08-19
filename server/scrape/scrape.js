const request = require('request');
const cheerio = require('cheerio');

const scrape = () => {
  const URL = 'https://fireemblem.gamepress.gg/heroes';
  console.log('Scraping', URL)
  request(URL, (error, response, html) => {
    if(!error && response.statusCode === 200) {
      const $ = cheerio.load(html)
      console.log($('.hero-list-row').length)
    } else {
      console.error('There was an error accessing the site \n', error.message)
    }
  }
)}

module.exports = scrape;