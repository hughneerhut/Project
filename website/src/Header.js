import React from 'react';

class Header extends React.Component {
  render() {
    return (
      <div id = "wrapper">
        <Sidebar/>  
      </div>
    );
  }
}
class Sidebar extends React.Component{
  render(){
    return (
      <ul className="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion" id="accordionSidebar">
        
        {/* Sidebar heading */}
        <a className="sidebar-brand d-flex align-items-center justify-content-center" href="index.html">
          <div className="sidebar-brand-icon rotate-n-15">
            <i className="fas fa-truck"></i>
          </div>
          <div className="sidebar-brand-text mx-3">Delivery Optimisation</div>
        </a>
        {/* End Sidebar heading */}
        <hr className = "sidebar-divider my-0"/>
        
        <NavItem link = "dashboard.js" name = "Dashboard" icon = "fa-tachometer-alt" active/>

        <NavItem link = "orders.js" name = "Orders" icon = "fa-table"/>
        
        <NavItem link = "generateRoute.js" name = "Generate delivery route" icon = "fa-route"/>
      </ul>
    );
  }
}
class NavItem extends React.Component{
  render(){
    return(
      <li className = {"nav-item " + (this.props.active ? "active" : "")}>
        <a className = "nav-link" href = {this.props.link}>
          <i className = {"fas fa-fw " + this.props.icon}></i>
          <span> {this.props.name}</span>
        </a>
      </li>
    );
  }
}

export default Header;
