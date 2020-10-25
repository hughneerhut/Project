import React from 'react';
import View from '../Components/View';
import ContentCard from '../Components/ContentCard';

class Orders extends React.Component {

  constructor(){
    super();
    this.state = {orders: []};
  }

  loadScript(src){
    const script = document.createElement("script");    
    script.async = true;    
    script.src = src;    
    document.body.appendChild(script);  
  }

  componentDidMount(){
    this.getOrders();
  }

  getOrders()
  {
    fetch('http://localhost:3001/orders')
    .then(response => {
      console.log(response);
      response.json().then(orders => {
        orders = orders.map(order => {
          return {...order, created: new Date(Date.parse(order.created)).toLocaleString()}
        })
        this.setState({orders: orders});
        this.loadScript("vendor/datatables/jquery.dataTables.min.js");
        this.loadScript("vendor/datatables/dataTables.bootstrap4.min.js");
        this.loadScript("js/demo/datatables-demo.js");
      });
    });
  }

  render() {
    return (
      <View title = "Orders">

        <ContentCard>
          <div class="table-responsive">
            <table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">
              <thead>
                <tr>
                  <th>Order #</th>
                  <th>Origin</th>
                  <th>Destination</th>
                  <th>Item QTY</th>
                  <th>Volume</th>
                  <th>Weight</th>
                  <th>Status</th>
                  <th>Ordered Date</th>
                </tr>
              </thead>
              <tfoot>
                <tr>
                  <th>Order #</th>
                  <th>Origin</th>
                  <th>Destination</th>
                  <th>Item QTY</th>
                  <th>Volume</th>
                  <th>Weight</th>
                  <th>Status</th>
                  <th>Ordered Date</th>
                </tr>
              </tfoot>
              <tbody>
                {this.state.orders.map(order => {
                  return(
                    <tr>
                      <td>{order.orderID}</td>
                      <td>{order.origin}</td>
                      <td>{order.destination}</td>
                      <td>{order.qty}</td>
                      <td>{order.volume}</td>
                      <td>{order.weight}</td>
                      <td>{order.status}</td>
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

export default Orders;
