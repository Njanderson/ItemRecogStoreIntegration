import React, { Component } from 'react';
import Webcam from 'react-webcam';
import Item from './Item';
//https://github.com/mozmorris/react-webcam
class Camera extends Component {

  constructor(props) {
    super(props);
    this.state = {
      isLoading: false,
    };
  }

  buttonClicked = () => {
    this.setState({isLoading : true});
    const imageSrc = this.webcam.getScreenshot();
    //console.log(imageSrc);

    this.postData(imageSrc)
      .then(data => {
        console.log(data); 
        this.setState({itemData: data, isLoading: false});
      });
  };

  postData = (data) => {
    return fetch('http://127.0.0.1:3000/infer', {
      method: 'POST',
      body: this.stripDataURL(data),
    })
      .then(response => {
        return response.json() 
      })
      .catch(err => {
        alert(err);
      })
  }

  stripDataURL = (data) => {
      return data.replace(/^data:image\/\w+;base64,/, "");
  }

  setRef = (webcam) => {
    this.webcam = webcam;
  }

  render() {
    const buttonStyle = {
      fontSize: '20px',
      width: '200px',
    };
    return (
      <div>
        <Webcam 
          ref={this.setRef}
          screenshotFormat="image/jpeg"
        />
      
        <div>
          <button style={buttonStyle} onClick={this.buttonClicked} >
            Take Photo 
          </button>
        </div>
          <Item data={this.state}/>
      </div>
    );
  }
}
export default Camera;
