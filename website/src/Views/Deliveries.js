import React from 'react';
import View from '../Components/View';
import ContentCard from '../Components/ContentCard';

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
        console.log("Hello");
        this.setState({orders: orders});
      }).catch(err => console.log(err));
    });
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
      </View>
    );
  }
}

export default Deliveries;
