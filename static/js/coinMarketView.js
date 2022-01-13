class CoinMarketView {
    _allData
    _data;
    _parentElement = document.querySelector('.coin-market');

    render(data) {
        this._data = data;
        const markup = this._generateMarkup();

        this._parentElement.insertAdjacentHTML('beforeend', markup);
    }

    renderMarkup(allData) {
        this.clear();
        this._allData = allData;

        console.log(this._allData);
        return this._allData.map(element => this.render(element)).join('')
    }

    _generateMarkup() {
        return `
                <td style="font-size: 11px;"> <img src="${this._data.image}" width="23"> ${this._data.symbol}</td>
                <td style="font-size: 12px;" class="coin_market">${this._data.current_price}</td>
                <td style="font-size: 1px" class="day_change">${this._data.price_change_persentage}</td>
        `
    }

    priceChangeColor() {
        const _allPriceChange = document.querySelectorAll('.day_change')
        _allPriceChange.forEach(num => {
            if (Number(num.textContent) > 0) {
                num.style.color = 'green';
                num.textContent = `▲${num.textContent}`;
            } else {
                num.style.color = 'red';
                num.textContent = `▼${num.textContent}`;
            }
        })
    }

    clear() {
        this._parentElement.innerHTML = '';
    }

}

export default new CoinMarketView();

