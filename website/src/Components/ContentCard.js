import React from 'react';

/*
  All of the cards
  Takes title as prop
  */
class ContentCard extends React.Component{
  render(){
    return(
      <div className = "row">
        <div className = "col-xl-12 col-md-6 mb-4">
          <div className = "card shadow">
            <div className = "card-body">
              <h6 className = "font-weight-bold text-primary">{this.props.title}</h6>
              <div className = "row no-gutters align-items-center">
                <div className = "col">
                  <div className = "row">
                    {this.props.children}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div> 
      </div>
    );
  }
}

export default ContentCard;
