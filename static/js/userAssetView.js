class UserAssetView {
    _data;
    _parentElement = document.querySelectorAll('.coin-icon')
    _coinProfit = document.querySelector('.coin_profit')


    render(data) {
        this._data = data
        console.log(Array.from(this._parentElement))
        console.log(this._data)
        Array.from(this._parentElement).map(ele => {
            const userAssetSymbol = ele.alt
            ele.src = this._data[userAssetSymbol]
        });
    }

    addHandlerUserAsset(handler) {
        if (window.location.pathname === '/dashboard') {
            if (Number(this._coinProfit.textContent) > 0) {
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