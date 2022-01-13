const COIN_GECKO_URL = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page=1&sparkline=false';
let lastBitcoin;

export const state = {
    result: [],
    allCoinImage: {},
}


const timeout = function (s) {
    return new Promise(function (_, reject) {
        setTimeout(function () {
            reject(new Error(`Request took too long! Timeout after ${s} second`));
        }, s * 1000);
    });
};

const _getData = async function (url) {
    try {
        const fetchData = fetch(url);
        const res = await Promise.race([fetchData, timeout(10)]);
        const result = await res.json();

        if (!res.ok) throw new Error(`something wrong.`);

        console.log(result);
        return result;

    } catch (err) {
        console.log(err);
    }
}

export const loadData = async function () {
    try {
        const newData = await _getData(COIN_GECKO_URL);
        let curBitcoinPrice = newData[0].current_price;

        state.result = newData.map(res => {
            return {
                id: res.id,
                symbol: res.symbol.toUpperCase(),
                name: res.name,
                image: res.image,
                current_price: res.current_price,
                price_change_persentage: res.price_change_percentage_24h.toFixed(2),
            }
        })

        lastBitcoin = document.querySelector('.coin_market');
        if (lastBitcoin !== null) {
            const lastBitcoinPrice = Number(lastBitcoin.textContent);
            console.log(lastBitcoinPrice, curBitcoinPrice);
            if (lastBitcoinPrice === curBitcoinPrice) {
                return 'same';
            }
        }

        return 'diff';

    } catch (err) {
        console.log(err);
    }
}

export const loadCoinImage = async function () {
    state.result.map(res => {
        return state.allCoinImage[res.symbol] = res.image
    })
}