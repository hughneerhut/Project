const Database = require("./Database");
const express = require("express");

const app = express();
const db = new Database();

app.get('/orders', function(req, res) {
  db.getOrders().then((result) => {
    console.log("List of orders requested.");
    res.send(result);
  }).catch(err => console.log(err));
});

app.get('/destinations', function(req, res) {
  db.getDestinations().then((result) => {
    console.log("List of destinations requested.");
    res.send(result.map(dest => dest.destination));
  }).catch(err => console.log(err));
});

app.get('/origins', function(req, res) {
  db.getOrigins().then((result) => {
    console.log("List of origins requested.");
    res.send(result.map(origin => origin.origin));
  }).catch(err => console.log(err));
});

app.listen(3001, () => {
  console.log("API Listening, go to http://localhost:3001/orders for list of orders");
});