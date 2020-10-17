import React from 'react';

/*
  All of the cards
  Takes title as prop
  */
class ContentCard extends React.Component{
  render(){
    return(
      <div class = "row">
        <div class = "col-xl-12 col-md-6 mb-4">
          <div class = "card shadow">
            <div class = "card-body">
              <h6 class = "font-weight-bold text-primary">{this.props.title}</h6>
              <div class = "row no-gutters align-items-center">
                <div class = "col">
                  <div class="row">
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
