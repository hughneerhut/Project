import React from 'react';
import {Route, Switch} from 'react-router-dom';

import Dashboard from './Views/Dashboard';
import Orders from './Views/Orders';
import GeneratDeliveries from './Views/GenerateDelivery';
import Deliveries from './Views/Deliveries';

const Main = () => {
  return (
    <Switch>
      <Route exact path = '/' component = {Dashboard}/>
      <Route exact path = '/orders' component = {Orders}/>
      <Route exact path = '/generateDeliveries' component = {GeneratDeliveries}/>
      <Route exact path = '/deliveries' component = {Deliveries}/>
    </Switch>
  );
}

export default Main;