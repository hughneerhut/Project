import React from 'react';
import View from '../Components/View';
import ContentCard from '../Components/ContentCard';
import { withRouter } from 'react-router-dom';

class GenerateDeliveries extends React.Component {

  constructor(props)
  {
    super(props);
    this.state = {
      locations: [],
      origin: '',
      destination: '',
      weight: 3000, //kg
      volume: 5000 //cm3
    };
    this.state.locations = this.getLocations();

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(event){
    this.props.history.push("/deliveries");
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
  }

  getLocations()
  {
    return ['Ringwood East VIC 3135', 'Ringwood VIC 3034', 'Mooroolbark VIC 3138'];
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
                  {this.state.locations.map(loc => {
                    return <option value = {loc}> {loc} </option>
                  })}
                </select>
              </label>
            </div>

            <div class = "form-group">
              <label>Destination
                <select class = "form-control" value = {this.state.destination} name = "destination" onChange = {this.handleChange}>
                  <option value = "" disabled selected>Select destination</option>
                  {this.state.locations.map(loc => {
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
