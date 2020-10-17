import React from 'react';
import View from '../Components/View';
import ContentCard from '../Components/ContentCard';

class Dashboard extends React.Component {
  render() {
    return (
      <View title = "Dashboard">
        <ContentCard title = "Delivery Stats">
          <DataCard title = "Today" data = "12" icon = "fa-truck" color = "primary"/>
          <DataCard title = "This Month" data = "300" icon = "fa-truck" color = "primary"/>
          <DataCard title = "This Year" data = "3600" icon = "fa-truck" color = "primary"/>
        </ContentCard>

        <ContentCard title = "Carbon Emission Stats">
          <DataCard title = "Today" data = "100kg" icon = "fa-tree" color = "info"/>
          <DataCard title = "This Month" data = "3,000kg" icon = "fa-tree" color = "info"/>
          <DataCard title = "This Year" data = "32,000kg" icon = "fa-tree" color = "info"/>
        </ContentCard>

        <ContentCard title = "Todays Delivery Progress">
          <div className = "col-xl-12 col-md-6 mb-1">
            <div className = "card shadow h-100 py-2">
              <div className = "card-body">
                <div className = "row no-gutters align-items-center">
                  <div className = "col-xl-12">
                    <div className = "progress">
                      <div className = "progress-bar bg-success" role="progressbar" style={{width: "50%"}} aria-valuenow="50" aria-valuemin="0" aria-valuemax="100">50%</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </ContentCard>

        <ContentCard title = "Annual Deliveries Overview">
          <div className = "chart-area">
            <canvas id="deliveriesChart"></canvas>
          </div>
        </ContentCard>
        
      </View>
    );
  }
}

/*
  Small data cards
  takes title, data, icon and border color.
*/
class DataCard extends React.Component{
  render(){
    return(
      <div className = "col-xl-4 col-md-6 mb-1">
        <div class={"card border-left-" + this.props.color + " shadow h-100 py-2"}>
          <div className = "card-body">
            <div className = "row no-gutters align-items-center">
              <div className = "col mr-2">
                <div class={"text-xs font-weight-bold text-"+ this.props.color +" text-uppercase mb-1"}>{this.props.title}</div>
                <div className = "h5 mb-0 font-weight-bold text-gray-800 text-center">{this.props.data}</div>
              </div>
              <div className = "col-auto">
                <i class={"fas "+this.props.icon+" fa-2x text-gray-300"}></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}
export default Dashboard;