/*
 * 1 - Monitoramento
 * 2 - Estratégia
 * 3 - Trade
*/
const express = require("express");
const axios = require("axios");
const cheerio = require("cheerio");
const port = 3010

async function getPrinceFeed() {
    try {
        const siteUrl = process.env.STREAM_URL
        const { data } = await axios({
            method: "GET",
            url: siteUrl
        })

        const $ = cheerio.load(data)
        const elemSelector = "#__next > div.sc-65dd1213-1.ipsZBU.global-layout-v2 > div.main-content > div.cmc-body-wrapper > div > div:nth-child(1) > div.sc-feda9013-2.dxcftz > table > tbody > tr"

        const keys = [
            "rank",
            "name",
            "price",
            "1h",
            "24h",
            "7d",
            "marketCap",
            "volume",
            "circSupl"
        ]

        const coinArr = []

        $(elemSelector).each((index, elem) => {
            let keyIndex = 0
            const coinObj = {}

            if(index <= 9) {
                $(elem).children().each((childIndex, childElem) => {
                    let tdValue = $(childElem).text()

                    if  (keyIndex === 1 || keyIndex === 6) {
                        tdValue = $('p:first-child',$(childElem).html()).text()
                    }
                    
                    if (tdValue) {
                        coinObj[keys[keyIndex]] = tdValue
                        keyIndex++
                    }
                })
                coinArr.push(coinObj)
            }
        })
        return coinArr
    } catch (err){
        console.error(err)
    }
}

const app = express()

app.get('/api/price-feed', async (req, res) => {
    try {
        const priceFeed = await getPrinceFeed()

        return res.status(200).json({
            result: priceFeed,
        })
    } catch(err) {
        return res.status(500).json({
            err: err.toString(),
        })
    }
})

app.listen(port, () => {
    console.log(`Running on port ${port}`)
})
