const puppeteer = require('puppeteer');

async function savePageAsPNG(url, outputFilePath) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  await page.goto(url, { waitUntil: 'networkidle0' });

  const bodyHandle = await page.$('body');
  const boundingBox = await bodyHandle.boundingBox();

  await page.screenshot({
    path: outputFilePath,
    clip: boundingBox,
  });

  await browser.close();

  console.log('Page saved as PNG:', outputFilePath);
}

// Example usage
const url = 'http://localhost:5100/';
const outputFilePath = 'output.png';

savePageAsPNG(url, outputFilePath);
