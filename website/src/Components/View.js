import React from 'react';
import Navigation from './Navigation';


class View extends React.Component {
  render() {
    return (
      <div id = "wrapper">
        <Navigation/>
        <div id="content-wrapper" className = "d-flex flex-column">
          <div id = "content">
            <div className = "container-fluid mt-4">
              <div className = "d-sm-flex align-items-center justify-content-between mb-4">
                <h1 className = "h3 mb-0 text-gray-800">{this.props.title}</h1>
              </div>
              {this.props.children}
            </div>
          </div>
          <footer className = "sticky-footer bg-white">
            <div className = "container my-auto">
              <div className = "copyright text-center my-auto">
                <span>Copyright &copy; Your Website 2020</span>
              </div>
            </div>
          </footer>
        </div>
      </div>
    );
  }
}


export default View;
