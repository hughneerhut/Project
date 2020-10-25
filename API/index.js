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

app.get('/truck', function(req, res){
  if(!req.query.origin || !req.query.dest)
    return res.status(400).send({message: "Origin / Destination not provided."});
  let origin = req.query.origin; //testing: 4164
  let destination = req.query.dest; //testing: 3029
  db.getTruck(origin, destination).then(result => {
    console.log("Truck requested for " + origin + " to " + destination);
    res.send(result);
  }).catch(err => console.log(err));
})

app.listen(3001, () => {
  console.log("API Listening, go to http://localhost:3001/orders for list of orders");
});