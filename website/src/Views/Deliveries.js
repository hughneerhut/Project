import React from 'react';
import View from '../Components/View';
import ContentCard from '../Components/ContentCard';

class Deliveries extends React.Component {
  loadScript(src){
    const script = document.createElement("script");    
    script.async = true;    
    script.src = src;    
    document.body.appendChild(script);  
  }

  componentDidMount(){
    this.loadScript("vendor/datatables/jquery.dataTables.min.js");
    this.loadScript("vendor/datatables/dataTables.bootstrap4.min.js");
    this.loadScript("js/demo/datatables-demo.js");
  }
  
  render() {
    return (
      <View title = "Deliveries">
        <ContentCard>
          <div class="table-responsive">
            <table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">
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
                <tr>
                  <td>1</td>
                  <td>12/12/2020</td>
                  <td>3135 VIC Australia</td>
                  <td>3138 VIC Australia</td>
                  <td>2</td>
                  <td>200cm<sup>3</sup></td>
                  <td>20kg</td>
                </tr>
              </tbody>
            </table>
          </div>
        </ContentCard>
      </View>
    );
  }
}

export default Deliveries;
