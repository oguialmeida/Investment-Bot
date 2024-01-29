/*
 * 1 - Monitoramento
 * 2 - Estratégia
 * 3 - Trade
*/
const express = require("express");
const axios = require("axios");
const cheerio = require("cheerio");

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
            "24",
            "7d",
            "marketCap",
            "volume",
            "circSupl"
        ]

        $(elemSelector).each((index, elem) => {
            if(index <= 50) {
                $(elem).children().each((childIndex, childElem)=>{
                    const tdValue = $(childElem).text()
                    
                    if (tdValue) {
                        console.log(tdValue)
                    }
                })
            }
        })
    } catch (err){
        console.error(err)
    }
}

getPrinceFeed()
