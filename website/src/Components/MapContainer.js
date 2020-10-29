/*global google*/
import React from "react";
import {
    GoogleApiWrapper,
    Map,
    DirectionsRenderer
} from "google-maps-react";
import Geocode from "react-geocode";

class MapContainer extends React.Component {
    constructor(props) {
        super(props);

        Geocode.setApiKey("");

        Geocode.setRegion("au");
        
        this.state = {
            stores: [Geocode.fromAddress("3134").then(response => { let { lat, lng } = response.result[0].geometry.location; }),
                     Geocode.fromAddress("3140").then(response => { let { lat, lng } = response.result[0].geometry.location; })]
        }


    }

    displayMarkers = () => {
        return this.state.stores.map((store, index) => {
            return <Marker key={index} id={index} position={{
                lat: store.lat,
                lng: store.lng
            }}
                onClick={() => console.log("You clicked me!")}/>
        })    
    }

    render() {
        
        /*const GoogleMapExample = withGoogleMap(props => (
            <GoogleMap
                defaultCenter={{ lat: 40.756795, lng: -73.954298 }}
                defaultZoom={13}
            >
                <DirectionsRenderer
                    directions={this.state.directions}
                />
            </GoogleMap>
        ));*/

        return (
            <div>
            <Map
               google={this.props.google}
               zoom={8}
               initialCenter={{lat: 47.444, lng: -122.176}}
               style={{ width: '1500px', height: '500px'}}
                >
                    {this.displayMarkers()}
                </Map>
            </div>
        );
    }
}

export default GoogleApiWrapper({
    apiKey: 'AIzaSyBxdno1s4DjUQ5e91-8nFbhfRa1x76BnKg'
})(MapContainer);
