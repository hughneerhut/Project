import React from 'react';
import View from '../Components/View';
import ContentCard from '../Components/ContentCard';
import DataCard from '../Components/DataCard';

class Deliveries extends React.Component {

  constructor(props){
    super(props);

    let origin = this.props.location.data ? this.props.location.data.origin : localStorage.getItem('origin');
    let destination = this.props.location.data ? this.props.location.data.destination : localStorage.getItem('destination');
    localStorage.setItem('origin', origin);
    localStorage.setItem('destination', destination);

    this.state = {
      orders: [],
      origin,
      destination
    }
  }


  componentDidMount(){
    this.getOrders();
  }

  getOrders()
  {
    fetch('http://localhost:3001/truck?origin=' + this.state.origin + '&dest=' + this.state.destination)
    .then(response => {
      console.log(response);
      response.json().then(orders => {
        orders = orders.map(order => {
          return {...order, created: new Date(Date.parse(order.created)).toLocaleString()}
        });
        this.setState({orders: orders});
      }).catch(err => console.log(err));
    });
  }

  getDeliveryWeight()
  {
    let weight = 0;
    this.state.orders.forEach(order => {
      weight += order.weight;
    });
    return weight;
  }

  getDeliveryVolume()
  {
    let volume = 0;
    this.state.orders.forEach(order => {
      volume += order.volume;
    })
    return volume;
  }

  getStops()
  {
    let stops = 0;
    let lastStop = 0;
    this.state.orders.forEach(order => {
      if(order.pickupIndex != lastStop)
      {
        stops++;
        lastStop = order.pickupIndex;
      }
    });
    return stops;
  }

  getItems()
  {
    let items = 0;
    this.state.orders.forEach(order => {
      items += order.qty;
    });
    return items;
  }
  
  render() {
    return (
      <View title = "Batched Delivery">
        <ContentCard title = "Delivery Information">
          <DataCard title = "Truck ID" 
              data = {this.state.orders.length != 0 ? this.state.orders[0].truckID : 0} 
              icon = "fa-truck" 
              color = "primary"/>
          <DataCard title = "Delivery Weight" data = {this.getDeliveryWeight() + "kg"} icon = "fa-anchor" color = "primary"/>
          <DataCard title = "Delivery Volume" data = {this.getDeliveryVolume() + "m3"} icon = "fa-volume-up" color = "primary"/>
          <DataCard title = "Total Orders" data = {this.state.orders.length} icon = "fa-shopping-cart" color = "primary"/>
          <DataCard title = "Total Stops" data = {this.getStops()} icon = "fa-stop" color = "primary"/>
          <DataCard title = "Total Items" data = {this.getItems()} icon = "fa-gift" color = "primary"/>
        </ContentCard>
        <ContentCard title = "Deliveries list">
          <div class="table-responsive">
            <table class="table table-bordered" width="100%" cellspacing="0">
              <thead>
                <tr>
                  <th>Order #</th>
                  <th>Delivery order</th>
                  <th>Origin</th>
                  <th>Destination</th>
                  <th>Item QTY</th>
                  <th>Volume</th>
                  <th>Weight</th>
                  <th>Ordered Date</th>
                </tr>
              </thead>
              <tbody>
                {this.state.orders.map(order => {
                  return(
                    <tr>
                      <td>{order.orderID}</td>
                      <td>{order.pickupIndex}</td>
                      <td>{order.origin}</td>
                      <td>{order.destination}</td>
                      <td>{order.qty}</td>
                      <td>{order.volume}</td>
                      <td>{order.weight}</td>
                      <td>{order.created}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </ContentCard>
        <ContentCard title = "Map">
          <img src = {require("../map.png")} width = "100%"/>
        </ContentCard>
      </View>
    );
  }
}

export default Deliveries;
