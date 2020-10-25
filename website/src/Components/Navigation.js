import React from 'react';
import { Link, useLocation} from "react-router-dom";

class Navigation extends React.Component {
  render() {
    return (
      <Sidebar/>  
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
        <NavItem link = "/" name = "Dashboard" icon = "fa-tachometer-alt" />

        <NavItem link = "/orders" name = "Orders" icon = "fa-table"/>
        
        <NavItem link = "/generateDeliveries" name = "Get Delivery Grouping" icon = "fa-route"/>
      </ul>
    );
  }
}
class NavItem extends React.Component{
  render(){
    return(
      <li className = {"nav-item " + (window.location.pathname == this.props.link ? "active" : "")}>
        <Link className = "nav-link" to = {this.props.link}>
          <i className = {"fas fa-fw " + this.props.icon}></i>
          <span> {this.props.name}</span>
        </Link>
      </li>
    );
  }
}

export default Navigation;
