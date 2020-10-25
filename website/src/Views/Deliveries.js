import React from 'react';
import View from '../Components/View';
import ContentCard from '../Components/ContentCard';

class Deliveries extends React.Component {

  constructor(props){
    super(props)
    // this.state = {
    //   origin: this.props.location.data.origin,
    //   destination: this.props.location.data.destination
    // }
  }

  getOrders()
  {
    let orders = [];
    orders.push({
      number: 1, 
      date: '12/12/2020', 
      origin: {value: '3135', display: '3135 VIC Australia'},
      destination: {value: '3138', display: '3138 VIC Australia' },
      item_qty: 2,
      volume: 200,
      weight: 200
    });
    return orders;
    // return orders.filter(order => 
    //   order.origin.value == this.state.origin && order.destination.value == this.state.destination);
  }
  
  render() {
    return (
      <View title = "Deliveries">
        <ContentCard>
          <div class="table-responsive">
            <table class="table table-bordered" width="100%" cellspacing="0">
              <thead>
                <tr>
                  <th>Order #</th>
                  <th>Ordered Date</th>
                  <th>Origin</th>
                  <th>Destination</th>
                  <th>Item QTY</th>
                  <th>Volume</th>
                  <th>Weight</th>
                </tr>
              </thead>
              <tfoot>
                <tr>
                  <th>Order #</th>
                  <th>Ordered Date</th>
                  <th>Origin</th>
                  <th>Destination</th>
                  <th>Item QTY</th>
                  <th>Volume</th>
                  <th>Weight</th>
                </tr>
              </tfoot>
              <tbody>
                {this.getOrders().map(order => {
                  return(
                    <tr>
                      <td>{order.number}</td>
                      <td>{order.date}</td>
                      <td>{order.origin.display}</td>
                      <td>{order.destination.display}</td>
                      <td>{order.item_qty}</td>
                      <td>{order.volume}</td>
                      <td>{order.weight}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </ContentCard>
      </View>
    );
  }
}

export default Deliveries;
