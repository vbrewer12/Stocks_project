document.addEventListener("DOMContentLoaded", () => { 
    console.log('Dashboard Running')
    
    let ticker = "AAPL"
    
    fetch(`/api/stockprices?selectedTicker=${ticker}`).then(res => res.json()).then(stockprice => {
       console.log(stockprice)
    })
})