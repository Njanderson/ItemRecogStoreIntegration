import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import Camera from './Camera';
import backgroundImage from './bg.jpg'

class App extends Component {
  render() {
    const logoStyle = {
      fontSize: '40px',
      paddingTop: '20px',
      paddingBottom: '20px',
      color: "#ffffff",
      fontFamily: "HelveticaNeue-Light",
    };
    const mainStyle = {
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      color: "#ffffff",
      fontFamily: "HelveticaNeue-Light",
    };
    return (
      <div className="App" style={{backgroundImage : `url(${backgroundImage})` , backgroundRepeat: 'repeat', backgroundSize: 'cover'}} >
        <div className="MainApp" style={mainStyle}>
          <div className="logo" style={logoStyle}>
            Welcome to the Vision Snack Store
          </div>
          <Camera/> 
        </div>
      </div>

    );
  }
}
export default App;
