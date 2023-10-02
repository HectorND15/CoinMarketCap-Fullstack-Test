
const div = document.getElementById('tester')

const updateChart = () => {
  fetch('/data')  // Obtener datos del servidor
    .then(response => response.json())
    .then(data => {
      const processedData = data.processedData;

      const timestamps = processedData.created_at;
      const btcPrices = processedData.BTC;
      const ethPrices = processedData.ETH;
      
      const btcTrace = {
        x: timestamps,
        y: btcPrices,
        mode: 'lines',
        name: 'BTC',
        line: {
          color: 'blue'
        }
      };
  
      // Create a trace for ETH prices
      const ethTrace = {
        x: timestamps,
        y: ethPrices,
        name: 'ETH',
        mode: 'lines',
        line: {
          color: 'red'
        }
      };
  
      // Data array containing both traces
      const data2 = [btcTrace];
  
      // Layout configuration for the chart
      const layout = {
        title: 'BTC Crypto Prices',
        xaxis: {
          title: '',
          showticklabels: false
        },
        yaxis: {
          title: 'Price'
        }
      };


      const layout1 = {
        title: 'ETH Crypto Prices',
        xaxis: {
          title: '',
          showticklabels: false
        },
        yaxis: {
          title: 'Price'
        }
      };
  
      // Render the chart using Plotly
      Plotly.newPlot('tester', [btcTrace], layout);
      Plotly.newPlot('tester1', [ethTrace], layout1);
    
    })
    .catch(error => {
      console.error('Error fetching data:', error);
    });
};

// Actualizar el gráfico cada segundo
updateChart();
setInterval(updateChart, 10000);
