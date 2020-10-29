/*global google*/
import React from "react";
import {
    GoogleApiWrapper,
    Map,
} from "google-maps-react";

class MapContainer extends React.Component {
    
    render() {
        
        return (
            <div>
            <Map
               google={this.props.google}
               zoom={8}
               initialCenter={{lat: 47.444, lng: -122.176}}
               style={{ width: '1615px', height: '800px'}}
                />
            </div>
        );
    }
}

export default GoogleApiWrapper({
    apiKey: 'AIzaSyBxdno1s4DjUQ5e91-8nFbhfRa1x76BnKg'
})(MapContainer);
