import React from 'react';
import {Route, Switch} from 'react-router-dom';

import Dashboard from './Views/Dashboard';
import Orders from './Views/Orders';
import Batched from './Views/Batched';
import GeneratDeliveries from './Views/GenerateDelivery';
import Deliveries from './Views/Deliveries';

class Main extends React.Component
{
  render(){
    return (
      <Switch>
        <Route exact path = '/' component = {Dashboard}/>
        <Route exact path = '/orders' component = {Orders}/>
        <Route exact path = '/batched' component = {Batched}/>
        <Route exact path = '/generateDeliveries' component = {GeneratDeliveries}/>
        <Route exact path = '/deliveries' component = {Deliveries}/>
      </Switch>
    );
  } 
}

export default Main;