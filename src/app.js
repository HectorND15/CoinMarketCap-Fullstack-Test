require('dotenv').config();
const express = require('express');
const engine = require('ejs-mate');
const mysql = require("mysql2");
const path = require('path');

const cnx = require('./cnx');
const app = express();

// setting the server
app.engine('ejs', engine);
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views' ));


const connect = () =>{
    pool.getConnection(err => {
        if(err) throw err;
        console.log("Successful database connection!");
    });
}

app.get("/data", (req,res) =>{
    cnx.pool.query("SELECT BTC, ETH, created_at FROM (SELECT * FROM price_table ORDER BY created_at DESC LIMIT 20) AS SUBQUERY ORDER BY created_at ASC", (err,rows) => {
        const processedData = {
            
            BTC: rows.map(item => parseFloat(item.BTC)),
            ETH: rows.map(item => parseFloat(item.ETH)),
            created_at: rows.map(item => new Date(item.created_at).toLocaleString())
          };
        res.json({
            processedData
        });
    });
    
});

//routes
app.use(require('./routes/index'));
//static files
app.use(express.static( path.join(__dirname, 'public' )));

// starting the server
const port = 3000;
app.listen(port, () => {
    console.log("server on port: ",port)
});

cnx.connect();