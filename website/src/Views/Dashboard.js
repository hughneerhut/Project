import React from 'react';
import View from '../Components/View';
import ContentCard from '../Components/ContentCard';
import DataCard from '../Components/DataCard';

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
        
      </View>
    );
  }
}

export default Dashboard;