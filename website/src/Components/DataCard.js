import React from 'react';

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

export default DataCard;
