// 
// Scripts
//
import coinMarketView from './coinMarketView.js'
import userAssetView from './userAssetView.js'
import { loadData, loadCoinImage, state } from './model.js'

const searchTrade = document.querySelector('.search_trade__btn')
const form = document.querySelector('.form')

// Fetch Market Data every 30 sec, if data is different
// page content will change without refresh.
window.setInterval(async function () {
    if (window.location.pathname === '/' || window.location.pathname === '/dashboard') {
        const data = await loadData()
        if (data === 'diff') {
            console.log('✨✨✨')
            coinMarketView.renderMarkup(state.result.slice(0, 30))
            coinMarketView.priceChangeColor()
        }
    }
}, 30000);

window.addEventListener('DOMContentLoaded', event => {
    if (searchTrade) {
        if (localStorage.getItem('form_hidden') === 'false') {
            form.classList.remove('hidden');
        }
    }
});

searchTrade.addEventListener('click', function () {
    form.classList.toggle('hidden');
    localStorage.setItem('form_hidden', true);
})

const controlUserAsset = function () {
    userAssetView.render(state.allCoinImage)
}

const init = async function () {
    await loadData()
    loadCoinImage()
    coinMarketView.renderMarkup(state.result.slice(0, 30))
    coinMarketView.priceChangeColor()
    userAssetView.addHandlerUserAsset(controlUserAsset)
}
init()