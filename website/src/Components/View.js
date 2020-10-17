import React from 'react';
import Navigation from './Navigation';


class View extends React.Component {
  render() {
    return (
      <div id = "wrapper">
        <Navigation/>
        <div id="content-wrapper" class="d-flex flex-column">
          <div id = "content">
            <div class = "container-fluid mt-4">
              <div class="d-sm-flex align-items-center justify-content-between mb-4">
                <h1 class="h3 mb-0 text-gray-800">{this.props.title}</h1>
              </div>
              {this.props.children}
            </div>
          </div>
        </div>
      </div>
    );
  }
}


export default View;
