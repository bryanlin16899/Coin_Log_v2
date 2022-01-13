const UNDEFINED_IMG_SRC = 'https://static.coingecko.com/s/nftgecko-96c331e407a0db62a497df2a5679723ae3926f8bbc12b2885486cb0405552d4e.png'

class UserAssetView {
    _data;
    _parentElement = document.querySelectorAll('.coin-icon')
    _coinProfit = document.querySelector('.coin_profit')
    _averagePrice = document.querySelector('.average_price')


    render(data) {
        this._data = data
        console.log(Array.from(this._parentElement))
        console.log(this._data)
        Array.from(this._parentElement).map(ele => {
            const userAssetSymbol = ele.alt
            if(this._data[userAssetSymbol] !== undefined){
                ele.src=this._data[userAssetSymbol]
            } else {
                ele.src=UNDEFINED_IMG_SRC
            }
            
        });
    }

    addHandlerUserAsset(handler) {
        if (window.location.pathname === '/dashboard'){
            if (Number(this._coinProfit.textContent) > 0){
                this._coinProfit.style.color = 'green';
                this._coinProfit.textContent = `▲${this._coinProfit.textContent} USD`;
            } else if (Number(this._coinProfit.textContent) < 0) {
                this._coinProfit.style.color = 'red';
                this._coinProfit.textContent = `▼${this._coinProfit.textContent} USD`;
            } else {
                this._coinProfit.textContent = `0`;
            }
            handler()
        }
    }
}

export default new UserAssetView();