import React from 'react';
import View from '../Components/View';
import ContentCard from '../Components/ContentCard';
import { withRouter } from 'react-router-dom';

class GenerateDeliveries extends React.Component {

  constructor(props)
  {
    super(props);
    this.state = {
      origins: [],
      destinations: [],
      origin: '',
      destination: '',
      weight: 3000, //kg
      volume: 5000 //cm3
    };
    
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  componentDidMount(){
    this.getLocations();
  }

  handleSubmit(event){
    this.props.history.push({
      pathname: "/deliveries",
      data: {
              origin: this.state.origin,
              destination: this.state.destination
            }
    });
    event.preventDefault();
  }


  handleChange(event){
    const target = event.target;
    const value = target.value;
    const name = target.name;

    this.setState({
      ...this.state,
      [name] : value
    });

    if(name == "origin")
      this.handleOriginChange(value);
  }

  handleOriginChange(origin){
    fetch('http://localhost:3001/destinations?origin='+origin)
    .then(response => {
      response.json().then(destinations => {
        this.setState({...this.state, destinations: destinations});
        document.getElementById("destination").style.display = "block";
      });
    });
  }

  getLocations()
  {
    fetch('http://localhost:3001/origins')
    .then(response => {
      response.json().then(origins => {
        this.setState({...this.state, origins: origins});
      });
    });
  }

  render() {
    return (
      <View title = "Generate Deliveries">
        <ContentCard>
          <form onSubmit={this.handleSubmit}>
            <div class = "form-group">
              <label>Starting Location
                <select class = "form-control" value = {this.state.origin} name = "origin" onChange = {this.handleChange}>
                  <option value = "" disabled selected>Select starting location</option>
                  {this.state.origins.map(loc => {
                    return <option value = {loc}> {loc} </option>
                  })}
                </select>
              </label>
            </div>

            <div class = "form-group" id = "destination" style = {{display: "none"}}> 
              <label>Destination
                <select class = "form-control" value = {this.state.destination} name = "destination" onChange = {this.handleChange}>
                  <option value = "" disabled selected>Select destination</option>
                  {this.state.destinations.map(loc => {
                    return <option value = {loc}> {loc} </option>
                  })}
                </select>
              </label>
            </div>
            
            <div class = "form-group">
              <button type = "submit" class = "btn btn-primary mb-2">Generate Deliveries</button>
            </div>
          </form>
        </ContentCard>
      </View>
    );
  }
}

export default GenerateDeliveries;
