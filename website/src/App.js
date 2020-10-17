import React from 'react';
import Navigation from './Components/Navigation.js';
import Main from './Main';

class App extends React.Component {
  render() {
    return (
      <div className="App">
        <div id = "wrapper">
          <Navigation/>
          <Main/>
        </div>
      </div>
    );
  }
}

export default App;
