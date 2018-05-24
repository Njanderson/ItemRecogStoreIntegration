import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import Camera from './Camera';
import backgroundImage from './bg.jpg'

class App extends Component {
  render() {
    const logoStyle = {
      fontSize: '30px'
    };
    const mainStyle = {
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
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

    
        /*        
        {
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to React</h1>
        </header>
        <p className="App-intro">
          To get started, edit hi <code>src/App.js</code> and save to reload.
        </p>
        }
        */
export default App;
